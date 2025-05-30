import os
import sys
import shutil
from PyInstaller import __main__ as pyi

def create_default_icon():
    # Create assets directory if it doesn't exist
    if not os.path.exists('frontend/assets'):
        os.makedirs('frontend/assets')
    
    # Create a simple icon if none exists
    icon_path = 'frontend/assets/icon.ico'
    if not os.path.exists(icon_path):
        try:
            from PIL import Image, ImageDraw
            # Create a 256x256 image with a blue background
            img = Image.new('RGB', (256, 256), color='#3498db')
            draw = ImageDraw.Draw(img)
            # Draw a simple "GS" text
            draw.text((128, 128), "GS", fill='white', anchor="mm")
            # Save as ICO
            img.save(icon_path, format='ICO')
        except Exception as e:
            print(f"Warning: Could not create default icon: {e}")
            icon_path = None
    return icon_path

def build_app():
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

    # PyInstaller arguments - simplified for speed
    args = [
        'kivy_app.py',  # Main script
        '--name=GS_Browser',  # App name
        '--onefile',  # Single executable
        '--noconsole',  # No console window
        '--clean',  # Clean PyInstaller cache
    ]

    # Run PyInstaller
    pyi.run(args)
    print("Build completed! Check the 'dist' directory for your executable.")

if __name__ == '__main__':
    build_app() 