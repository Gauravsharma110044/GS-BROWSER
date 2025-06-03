from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from login_screen import LoginScreen
from profile_screen import ProfileScreen
from file_manager_screen import FileManagerScreen
from app_files_screen import AppFilesScreen

class MainApp(App):
    def build(self):
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(FileManagerScreen(name='file_manager'))
        sm.add_widget(AppFilesScreen(name='app_files'))
        
        return sm

if __name__ == '__main__':
    MainApp().run() 