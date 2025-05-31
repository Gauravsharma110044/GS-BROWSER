from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.webview import WebView
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.listview import ListView, ListItemButton
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
import os
import json
from datetime import datetime
import requests
from urllib.parse import urlparse

class BookmarkButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '★'
        self.size_hint_x = 0.1
        self.bind(on_press=self.toggle_bookmark)

    def toggle_bookmark(self, instance):
        browser = App.get_running_app()
        current_tab = browser.tab_panel.current_tab
        url = current_tab.url_input.text
        title = current_tab.webview.title or url
        
        if browser.is_bookmarked(url):
            browser.remove_bookmark(url)
            self.text = '☆'
        else:
            browser.add_bookmark(url, title)
            self.text = '★'

class HistoryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'History'
        self.size_hint_x = 0.1
        self.bind(on_press=self.show_history)

    def show_history(self, instance):
        browser = App.get_running_app()
        content = BoxLayout(orientation='vertical')
        list_view = ListView()
        
        for entry in browser.get_history():
            btn = ListItemButton(text=f"{entry['title']} - {entry['time']}")
            btn.bind(on_press=lambda x, url=entry['url']: self.load_url(url))
            list_view.add_widget(btn)
            
        content.add_widget(list_view)
        popup = Popup(title='History', content=content, size_hint=(0.8, 0.8))
        popup.open()

    def load_url(self, url):
        browser = App.get_running_app()
        browser.tab_panel.current_tab.url_input.text = url
        browser.tab_panel.current_tab.load_url()

class DownloadManager:
    def __init__(self):
        self.downloads = []
        self.download_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'GS_Browser')
        os.makedirs(self.download_dir, exist_ok=True)

    def download_file(self, url):
        try:
            response = requests.get(url, stream=True)
            filename = os.path.basename(urlparse(url).path) or 'download'
            filepath = os.path.join(self.download_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.downloads.append({
                'url': url,
                'filename': filename,
                'path': filepath,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return True
        except Exception as e:
            print(f"Download error: {e}")
            return False

class BrowserTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Navigation bar
        self.nav_bar = BoxLayout(size_hint_y=None, height=40)
        self.url_input = TextInput(
            multiline=False,
            size_hint_x=0.6,
            hint_text='Enter URL or search term'
        )
        self.go_button = Button(
            text='Go',
            size_hint_x=0.1,
            on_press=self.load_url
        )
        self.refresh_button = Button(
            text='↻',
            size_hint_x=0.1,
            on_press=self.refresh_page
        )
        self.bookmark_button = BookmarkButton()
        self.history_button = HistoryButton()
        
        self.nav_bar.add_widget(self.url_input)
        self.nav_bar.add_widget(self.go_button)
        self.nav_bar.add_widget(self.refresh_button)
        self.nav_bar.add_widget(self.bookmark_button)
        self.nav_bar.add_widget(self.history_button)
        
        # Web view
        self.webview = WebView()
        
        self.layout.add_widget(self.nav_bar)
        self.layout.add_widget(self.webview)
        self.add_widget(self.layout)
        
        # Bind enter key to load URL
        self.url_input.bind(on_text_validate=self.load_url)
        
    def load_url(self, *args):
        url = self.url_input.text
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        self.webview.url = url
        App.get_running_app().add_to_history(url, self.webview.title)
        
    def refresh_page(self, *args):
        self.webview.reload()

class BrowserApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('browser_data.json')
        self.download_manager = DownloadManager()
        
    def build(self):
        # Set window size
        Window.size = (1024, 768)
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Tab panel
        self.tab_panel = TabbedPanel(do_default_tab=False)
        
        # Add first tab
        self.add_new_tab()
        
        # Add tab button
        self.new_tab_button = Button(
            text='+',
            size_hint_x=None,
            width=50,
            on_press=self.add_new_tab
        )
        
        self.layout.add_widget(self.tab_panel)
        self.layout.add_widget(self.new_tab_button)
        
        return self.layout
    
    def add_new_tab(self, *args):
        tab = BrowserTab(text='New Tab')
        self.tab_panel.add_widget(tab)
        self.tab_panel.switch_to(tab)

    def add_bookmark(self, url, title):
        bookmarks = self.store.get('bookmarks', {})
        bookmarks[url] = {'title': title, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.store.put('bookmarks', **bookmarks)

    def remove_bookmark(self, url):
        bookmarks = self.store.get('bookmarks', {})
        if url in bookmarks:
            del bookmarks[url]
            self.store.put('bookmarks', **bookmarks)

    def is_bookmarked(self, url):
        bookmarks = self.store.get('bookmarks', {})
        return url in bookmarks

    def add_to_history(self, url, title):
        history = self.store.get('history', [])
        history.append({
            'url': url,
            'title': title or url,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        # Keep only last 100 entries
        history = history[-100:]
        self.store.put('history', entries=history)

    def get_history(self):
        return self.store.get('history', {}).get('entries', [])

if __name__ == '__main__':
    BrowserApp().run()
