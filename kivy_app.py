from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.webview import WebView
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
import os

class BrowserTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Navigation bar
        self.nav_bar = BoxLayout(size_hint_y=None, height=40)
        self.url_input = TextInput(
            multiline=False,
            size_hint_x=0.8,
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
        
        self.nav_bar.add_widget(self.url_input)
        self.nav_bar.add_widget(self.go_button)
        self.nav_bar.add_widget(self.refresh_button)
        
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
        
    def refresh_page(self, *args):
        self.webview.reload()

class BrowserApp(App):
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

if __name__ == '__main__':
    BrowserApp().run()
