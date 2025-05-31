import firebase_admin
from firebase_admin import credentials, db
import json
import os

def initialize_firebase():
    """Initialize Firebase with credentials"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Initialize Firebase with your credentials
            cred = credentials.Certificate('gs-browser-75739-firebase-adminsdk-fbsvc-dbd0e70ba0.json')
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gs-browser-75739-default-rtdb.firebaseio.com'  # Your project's database URL
            })
        return True
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        return False

def get_database():
    """Get database reference"""
    try:
        return db.reference('/')
    except Exception as e:
        print(f"Error getting database reference: {str(e)}")
        return None

# Database structure
DATABASE_STRUCTURE = {
    'users': {
        'user_id': {
            'profile': {
                'username': '',
                'email': '',
                'created_at': '',
                'last_login': ''
            },
            'settings': {
                'theme': 'light',
                'notifications': True,
                'language': 'en'
            }
        }
    },
    'app_data': {
        'version': '',
        'updates': {
            'latest_version': '',
            'release_notes': '',
            'download_url': ''
        },
        'statistics': {
            'total_users': 0,
            'active_users': 0,
            'downloads': 0
        }
    },
    'feedback': {
        'feedback_id': {
            'user_id': '',
            'type': '',
            'message': '',
            'timestamp': '',
            'status': 'pending'
        }
    }
}

def setup_database():
    """Set up initial database structure"""
    try:
        db_ref = get_database()
        if db_ref:
            # Set up initial structure
            db_ref.set(DATABASE_STRUCTURE)
            print("Database structure initialized successfully")
            return True
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return False

if __name__ == "__main__":
    if initialize_firebase():
        setup_database() 