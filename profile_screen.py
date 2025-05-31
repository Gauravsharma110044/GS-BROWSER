from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from firebase_auth import FirebaseAuth

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth = FirebaseAuth()
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title
        title = Label(text='Profile Settings', size_hint_y=None, height=50, font_size=24)
        layout.add_widget(title)

        # Create scrollable content
        scroll = ScrollView()
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Profile Section
        profile_section = self.create_section('Profile Information')
        content.add_widget(profile_section)

        # Username
        username_layout = BoxLayout(size_hint_y=None, height=40)
        username_layout.add_widget(Label(text='Username:'))
        self.username_input = TextInput(multiline=False)
        username_layout.add_widget(self.username_input)
        content.add_widget(username_layout)

        # Email (read-only)
        email_layout = BoxLayout(size_hint_y=None, height=40)
        email_layout.add_widget(Label(text='Email:'))
        self.email_label = Label(text='')
        email_layout.add_widget(self.email_label)
        content.add_widget(email_layout)

        # Settings Section
        settings_section = self.create_section('Settings')
        content.add_widget(settings_section)

        # Theme
        theme_layout = BoxLayout(size_hint_y=None, height=40)
        theme_layout.add_widget(Label(text='Theme:'))
        self.theme_spinner = Spinner(
            text='Light',
            values=('Light', 'Dark', 'System'),
            size_hint_y=None,
            height=40
        )
        theme_layout.add_widget(self.theme_spinner)
        content.add_widget(theme_layout)

        # Notifications
        notif_layout = BoxLayout(size_hint_y=None, height=40)
        notif_layout.add_widget(Label(text='Notifications:'))
        self.notif_switch = Switch(active=True)
        notif_layout.add_widget(self.notif_switch)
        content.add_widget(notif_layout)

        # Language
        lang_layout = BoxLayout(size_hint_y=None, height=40)
        lang_layout.add_widget(Label(text='Language:'))
        self.lang_spinner = Spinner(
            text='English',
            values=('English', 'Spanish', 'French', 'German'),
            size_hint_y=None,
            height=40
        )
        lang_layout.add_widget(self.lang_spinner)
        content.add_widget(lang_layout)

        # Privacy Section
        privacy_section = self.create_section('Privacy')
        content.add_widget(privacy_section)

        # Profile Visibility
        visibility_layout = BoxLayout(size_hint_y=None, height=40)
        visibility_layout.add_widget(Label(text='Profile Visible:'))
        self.visibility_switch = Switch(active=True)
        visibility_layout.add_widget(self.visibility_switch)
        content.add_widget(visibility_layout)

        # Online Status
        status_layout = BoxLayout(size_hint_y=None, height=40)
        status_layout.add_widget(Label(text='Show Online Status:'))
        self.status_switch = Switch(active=True)
        status_layout.add_widget(self.status_switch)
        content.add_widget(status_layout)

        # Analytics Section
        analytics_section = self.create_section('Analytics')
        content.add_widget(analytics_section)

        # Activity Graph
        self.activity_graph = self.create_activity_graph()
        content.add_widget(self.activity_graph)

        # File Manager Button
        file_manager_btn = Button(
            text='File Manager',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        file_manager_btn.bind(on_press=self.open_file_manager)
        content.add_widget(file_manager_btn)

        # App Files Button
        app_files_btn = Button(
            text='App Files',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        app_files_btn.bind(on_press=self.open_app_files)
        content.add_widget(app_files_btn)

        # Save Button
        save_btn = Button(
            text='Save Changes',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        save_btn.bind(on_press=self.save_changes)
        content.add_widget(save_btn)

        # Logout Button
        logout_btn = Button(
            text='Logout',
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        logout_btn.bind(on_press=self.logout)
        content.add_widget(logout_btn)

        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)

        # Load user data
        self.load_user_data()

    def create_section(self, title):
        section = BoxLayout(orientation='vertical', size_hint_y=None, height=40)
        section.add_widget(Label(
            text=title,
            size_hint_y=None,
            height=40,
            font_size=18,
            bold=True
        ))
        return section

    def create_activity_graph(self):
        # Create a figure for the activity graph
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.set_title('Login Activity')
        ax.set_xlabel('Date')
        ax.set_ylabel('Logins')
        
        # Create the canvas
        canvas = FigureCanvasKivyAgg(fig)
        return canvas

    def load_user_data(self):
        user_data = self.auth.get_current_user()
        if user_data:
            profile = user_data.get('profile', {})
            settings = user_data.get('settings', {})
            privacy = settings.get('privacy', {})
            
            # Set profile data
            self.username_input.text = profile.get('username', '')
            self.email_label.text = profile.get('email', '')
            
            # Set settings
            self.theme_spinner.text = settings.get('theme', 'Light').capitalize()
            self.notif_switch.active = settings.get('notifications', True)
            self.lang_spinner.text = settings.get('language', 'English').capitalize()
            
            # Set privacy settings
            self.visibility_switch.active = privacy.get('profile_visible', True)
            self.status_switch.active = privacy.get('show_online_status', True)
            
            # Update activity graph
            self.update_activity_graph()

    def update_activity_graph(self):
        analytics = self.auth.get_user_analytics()
        if analytics and 'activities' in analytics:
            # Process activity data
            dates = []
            counts = []
            # Add your activity processing logic here
            
            # Update the graph
            ax = self.activity_graph.figure.axes[0]
            ax.clear()
            ax.plot(dates, counts)
            ax.set_title('Login Activity')
            ax.set_xlabel('Date')
            ax.set_ylabel('Logins')
            self.activity_graph.draw()

    def save_changes(self, instance):
        # Update profile
        profile_data = {
            'username': self.username_input.text
        }
        
        # Update settings
        settings_data = {
            'theme': self.theme_spinner.text.lower(),
            'notifications': self.notif_switch.active,
            'language': self.lang_spinner.text.lower(),
            'privacy': {
                'profile_visible': self.visibility_switch.active,
                'show_online_status': self.status_switch.active
            }
        }
        
        # Save to Firebase
        if self.auth.update_user_profile(profile_data) and self.auth.update_user_settings(settings_data):
            self.show_success("Changes saved successfully!")
        else:
            self.show_error("Error saving changes")

    def logout(self, instance):
        if self.auth.sign_out():
            self.manager.current = 'login'
        else:
            self.show_error("Error signing out")

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

    def open_file_manager(self, instance):
        self.manager.current = 'file_manager'

    def open_app_files(self, instance):
        self.manager.current = 'app_files'

if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager
    
    class ProfileApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(ProfileScreen(name='profile'))
            return sm
    
    ProfileApp().run() 