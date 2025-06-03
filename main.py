from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

# Import your screen classes
from screens.login import LoginScreen
from screens.permission import PermissionScreen
from screens.home import HomeScreen
from screens.add import AddSpotScreen
from screens.spots import SafeSpotsScreen
from screens.emergency import EmergencyContactsScreen
from screens.events import EventsScreen
from screens.settings import SettingsScreen
from screens.about import AboutScreen
from screens.comments import CommentsScreen
from screens.gallery import ImageGalleryScreen

class SafeSpotApp(App):
    def build(self):
        self.title = "SafeSpot"
        self.logged_in = False  # Tracks if user is logged in

        sm = ScreenManager(transition=NoTransition())

        # Add all screens
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(PermissionScreen(name='permission'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddSpotScreen(name='add'))
        sm.add_widget(SafeSpotsScreen(name='spots'))
        sm.add_widget(EmergencyContactsScreen(name='emergency'))
        sm.add_widget(EventsScreen(name='events'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(AboutScreen(name='about'))
        sm.add_widget(CommentsScreen(name='comments'))
        sm.add_widget(ImageGalleryScreen(name='gallery'))

        # Start on login screen
        sm.current = 'login'
        return sm

if __name__ == '__main__':
    SafeSpotApp().run()