from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import os
import json
from datetime import datetime
from firebase_auth import FirebaseAuth

class AppFilesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth = FirebaseAuth()
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title
        title = Label(text='App Files Manager', size_hint_y=None, height=50, font_size=24)
        layout.add_widget(title)

        # Add New File Section
        add_section = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        
        # File Name Input
        name_layout = BoxLayout(size_hint_y=None, height=40)
        name_layout.add_widget(Label(text='File Name:', size_hint_x=0.3))
        self.file_name_input = TextInput(multiline=False, size_hint_x=0.7)
        name_layout.add_widget(self.file_name_input)
        add_section.add_widget(name_layout)

        # File Type Selection
        type_layout = BoxLayout(size_hint_y=None, height=40)
        type_layout.add_widget(Label(text='File Type:', size_hint_x=0.3))
        self.file_type_spinner = Spinner(
            text='Python',
            values=('Python', 'JavaScript', 'HTML', 'CSS', 'JSON', 'Text', 'Other'),
            size_hint_x=0.7
        )
        type_layout.add_widget(self.file_type_spinner)
        add_section.add_widget(type_layout)

        # File Content Input
        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        content_layout.add_widget(Label(text='File Content:', size_hint_y=None, height=30))
        self.file_content_input = TextInput(multiline=True, size_hint_y=None, height=70)
        content_layout.add_widget(self.file_content_input)
        add_section.add_widget(content_layout)

        # Add File Button
        add_btn = Button(
            text='Add File',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        add_btn.bind(on_press=self.add_file)
        add_section.add_widget(add_btn)

        layout.add_widget(add_section)

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

    def add_file(self, instance):
        name = self.file_name_input.text.strip()
        file_type = self.file_type_spinner.text
        content = self.file_content_input.text.strip()

        if not name or not content:
            self.show_error("Please fill in all fields")
            return

        # Create file data
        file_data = {
            'name': name,
            'type': file_type,
            'content': content,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        # Save to database
        if self.auth.save_app_file(file_data):
            self.show_success(f"File '{name}' added successfully")
            self.clear_inputs()
            self.load_files()
        else:
            self.show_error("Error adding file")

    def load_files(self):
        self.files_grid.clear_widgets()
        files = self.auth.get_app_files()
        
        for file in files:
            file_layout = BoxLayout(size_hint_y=None, height=100)
            
            # File info
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(text=file['name'], size_hint_y=None, height=30))
            info.add_widget(Label(
                text=f"Type: {file['type']} | Updated: {datetime.fromisoformat(file['updated_at']).strftime('%Y-%m-%d %H:%M')}",
                size_hint_y=None,
                height=30
            ))
            info.add_widget(Label(
                text=f"Content: {file['content'][:50]}...",
                size_hint_y=None,
                height=30
            ))
            file_layout.add_widget(info)
            
            # Buttons
            buttons = BoxLayout(size_hint_x=None, width=200, spacing=5)
            
            edit_btn = Button(
                text='Edit',
                size_hint_x=None,
                width=95,
                background_color=(0.2, 0.6, 0.8, 1)
            )
            edit_btn.bind(on_press=lambda x, f=file: self.edit_file(f))
            
            delete_btn = Button(
                text='Delete',
                size_hint_x=None,
                width=95,
                background_color=(0.8, 0.2, 0.2, 1)
            )
            delete_btn.bind(on_press=lambda x, f=file: self.delete_file(f))
            
            buttons.add_widget(edit_btn)
            buttons.add_widget(delete_btn)
            file_layout.add_widget(buttons)
            
            self.files_grid.add_widget(file_layout)

    def edit_file(self, file):
        # Populate inputs with file data
        self.file_name_input.text = file['name']
        self.file_type_spinner.text = file['type']
        self.file_content_input.text = file['content']

    def delete_file(self, file):
        if self.auth.delete_app_file(file['name']):
            self.show_success(f"File '{file['name']}' deleted successfully")
            self.load_files()
        else:
            self.show_error("Error deleting file")

    def clear_inputs(self):
        self.file_name_input.text = ''
        self.file_content_input.text = ''
        self.file_type_spinner.text = 'Python'

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
    
    class AppFilesApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(AppFilesScreen(name='app_files'))
            return sm
    
    AppFilesApp().run() 