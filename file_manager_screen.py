from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.utils import platform
import os
from datetime import datetime
from firebase_auth import FirebaseAuth

class FileManagerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth = FirebaseAuth()
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title
        title = Label(text='File Manager', size_hint_y=None, height=50, font_size=24)
        layout.add_widget(title)

        # Upload Button
        upload_btn = Button(
            text='Upload File',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        upload_btn.bind(on_press=self.show_upload_dialog)
        layout.add_widget(upload_btn)

        # Files List
        scroll = ScrollView()
        self.files_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.files_grid.bind(minimum_height=self.files_grid.setter('height'))
        scroll.add_widget(self.files_grid)
        layout.add_widget(scroll)

        # Back Button
        back_btn = Button(
            text='Back to Profile',
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)
        self.load_files()

    def show_upload_dialog(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # File chooser
        file_chooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*']
        )
        content.add_widget(file_chooser)

        # Buttons
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        upload_btn = Button(
            text='Upload',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        upload_btn.bind(on_press=lambda x: self.upload_file(file_chooser.selection))
        
        cancel_btn = Button(
            text='Cancel',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        buttons.add_widget(upload_btn)
        buttons.add_widget(cancel_btn)
        content.add_widget(buttons)

        popup = Popup(
            title='Choose File to Upload',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()

    def upload_file(self, selection):
        if not selection:
            self.show_error("Please select a file")
            return

        file_path = selection[0]
        result = self.auth.upload_file(file_path)
        
        if result:
            self.show_success(f"File uploaded successfully: {result['name']}")
            self.load_files()
        else:
            self.show_error("Error uploading file")

    def load_files(self):
        self.files_grid.clear_widgets()
        files = self.auth.list_files()
        
        for file in files:
            file_layout = BoxLayout(size_hint_y=None, height=50)
            
            # File info
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(text=file['name'], size_hint_y=None, height=25))
            info.add_widget(Label(
                text=f"Uploaded: {datetime.fromisoformat(file['uploaded_at']).strftime('%Y-%m-%d %H:%M')}",
                size_hint_y=None,
                height=25
            ))
            file_layout.add_widget(info)
            
            # Buttons
            buttons = BoxLayout(size_hint_x=None, width=200, spacing=5)
            
            download_btn = Button(
                text='Download',
                size_hint_x=None,
                width=95,
                background_color=(0.2, 0.6, 0.8, 1)
            )
            download_btn.bind(on_press=lambda x, path=file['path']: self.download_file(path))
            
            delete_btn = Button(
                text='Delete',
                size_hint_x=None,
                width=95,
                background_color=(0.8, 0.2, 0.2, 1)
            )
            delete_btn.bind(on_press=lambda x, path=file['path']: self.delete_file(path))
            
            buttons.add_widget(download_btn)
            buttons.add_widget(delete_btn)
            file_layout.add_widget(buttons)
            
            self.files_grid.add_widget(file_layout)

    def download_file(self, storage_path):
        # Create downloads directory if it doesn't exist
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        # Get file name from storage path
        filename = os.path.basename(storage_path)
        local_path = os.path.join(download_dir, filename)
        
        if self.auth.download_file(storage_path, local_path):
            self.show_success(f"File downloaded to: {local_path}")
        else:
            self.show_error("Error downloading file")

    def delete_file(self, storage_path):
        if self.auth.delete_file(storage_path):
            self.show_success("File deleted successfully")
            self.load_files()
        else:
            self.show_error("Error deleting file")

    def go_back(self, instance):
        self.manager.current = 'profile'

    def show_error(self, message):
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

    def show_success(self, message):
        popup = Popup(
            title='Success',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager
    
    class FileManagerApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(FileManagerScreen(name='file_manager'))
            return sm
    
    FileManagerApp().run() 