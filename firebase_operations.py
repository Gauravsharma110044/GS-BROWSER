from firebase_config import initialize_firebase, get_database
from datetime import datetime
import uuid

class FirebaseOperations:
    def __init__(self):
        initialize_firebase()
        self.db = get_database()

    def create_user(self, username, email):
        """Create a new user in the database"""
        try:
            user_id = str(uuid.uuid4())
            user_data = {
                'profile': {
                    'username': username,
                    'email': email,
                    'created_at': datetime.now().isoformat(),
                    'last_login': datetime.now().isoformat()
                },
                'settings': {
                    'theme': 'light',
                    'notifications': True,
                    'language': 'en'
                }
            }
            self.db.child('users').child(user_id).set(user_data)
            return user_id
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    def update_app_version(self, version, release_notes, download_url):
        """Update app version information"""
        try:
            update_data = {
                'version': version,
                'updates': {
                    'latest_version': version,
                    'release_notes': release_notes,
                    'download_url': download_url
                }
            }
            self.db.child('app_data').update(update_data)
            return True
        except Exception as e:
            print(f"Error updating app version: {str(e)}")
            return False

    def submit_feedback(self, user_id, feedback_type, message):
        """Submit user feedback"""
        try:
            feedback_id = str(uuid.uuid4())
            feedback_data = {
                'user_id': user_id,
                'type': feedback_type,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            }
            self.db.child('feedback').child(feedback_id).set(feedback_data)
            return feedback_id
        except Exception as e:
            print(f"Error submitting feedback: {str(e)}")
            return None

    def update_user_settings(self, user_id, settings):
        """Update user settings"""
        try:
            self.db.child('users').child(user_id).child('settings').update(settings)
            return True
        except Exception as e:
            print(f"Error updating user settings: {str(e)}")
            return False

    def get_user_data(self, user_id):
        """Get user data"""
        try:
            return self.db.child('users').child(user_id).get().val()
        except Exception as e:
            print(f"Error getting user data: {str(e)}")
            return None

    def update_statistics(self, stats):
        """Update app statistics"""
        try:
            self.db.child('app_data').child('statistics').update(stats)
            return True
        except Exception as e:
            print(f"Error updating statistics: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    firebase_ops = FirebaseOperations()
    
    # Example: Create a new user
    user_id = firebase_ops.create_user("test_user", "test@example.com")
    
    # Example: Update app version
    firebase_ops.update_app_version(
        "1.0.0",
        "Initial release",
        "https://example.com/download"
    )
    
    # Example: Submit feedback
    feedback_id = firebase_ops.submit_feedback(
        user_id,
        "bug",
        "Found an issue with the app"
    ) 