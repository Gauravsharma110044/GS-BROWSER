import os
import json
import requests
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtCore import QUrl

class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters = set()
        self.load_filters()
        
    def load_filters(self):
        """Load ad-blocking filters from EasyList"""
        try:
            # Download EasyList
            response = requests.get('https://easylist.to/easylist/easylist.txt')
            if response.status_code == 200:
                # Parse filters
                for line in response.text.split('\n'):
                    if line.startswith('||') or line.startswith('|http'):
                        self.filters.add(line.strip())
                
                # Save filters locally
                with open('adblock/filters.json', 'w') as f:
                    json.dump(list(self.filters), f)
        except Exception as e:
            print(f"Error loading ad filters: {e}")
            # Try to load from local file if download fails
            try:
                with open('adblock/filters.json', 'r') as f:
                    self.filters = set(json.load(f))
            except:
                print("No local filters found")
    
    def interceptRequest(self, info):
        """Intercept and block ad requests"""
        url = info.requestUrl().toString()
        
        # Check if URL matches any filter
        for filter_rule in self.filters:
            if filter_rule in url:
                info.block(True)
                return 