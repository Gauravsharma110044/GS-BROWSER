import os
import json
import requests
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineScript
from PyQt5.QtCore import QUrl
from adblockparser import AdblockRules

POPULAR_SITE_CSS = {
    'youtube.com': '''
    /* Hide YouTube video ads */
    .video-ads, .ytp-ad-module, .ytp-ad-player-overlay, .ytp-ad-overlay-slot, .ytp-ad-progress-list {
        display: none !important;
    }
    ''',
    'facebook.com': '''
    /* Hide Facebook sponsored posts */
    [aria-label="Sponsored"], [data-pagelet^="FeedUnit_"] [role="article"] [aria-label="Sponsored"] {
        display: none !important;
    }
    ''',
    'twitter.com': '''
    /* Hide Twitter promoted tweets */
    article [data-testid="placementTracking"] {
        display: none !important;
    }
    '''
}

class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters = []
        self.rules = None
        self.load_filters()
        
    def load_filters(self):
        """Load ad-blocking filters from EasyList and initialize adblockparser."""
        try:
            # Download EasyList
            response = requests.get('https://easylist.to/easylist/easylist.txt')
            if response.status_code == 200:
                self.filters = [line.strip() for line in response.text.split('\n') if line and not line.startswith('!')]
                # Save filters locally
                with open('adblock/filters.json', 'w') as f:
                    json.dump(self.filters, f)
            else:
                raise Exception('Failed to download EasyList')
        except Exception as e:
            print(f"Error loading ad filters: {e}")
            # Try to load from local file if download fails
            try:
                with open('adblock/filters.json', 'r') as f:
                    self.filters = json.load(f)
            except:
                print("No local filters found")
        # Initialize adblockparser rules
        self.rules = AdblockRules(self.filters)
    
    def interceptRequest(self, info):
        """Intercept and block ad requests using adblockparser."""
        url = info.requestUrl().toString()
        if self.rules and self.rules.should_block(url):
            info.block(True)
            return
    
    @staticmethod
    def get_cosmetic_script_for_url(url):
        """Return a QWebEngineScript to inject CSS for popular sites."""
        for domain, css in POPULAR_SITE_CSS.items():
            if domain in url:
                script = QWebEngineScript()
                script.setName(f"adblock_css_{domain}")
                script.setInjectionPoint(QWebEngineScript.DocumentReady)
                script.setRunsOnSubFrames(True)
                script.setWorldId(QWebEngineScript.MainWorld)
                script.setSourceCode(f"var style = document.createElement('style'); style.innerHTML = `{css}`; document.head.appendChild(style);")
                return script
        return None 