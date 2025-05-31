from setuptools import setup, find_packages

setup(
    name="gs-browser",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
        'PyQtWebEngine>=5.15.0',
        'requests>=2.25.1',
        'google-auth>=2.3.0',
        'google-auth-oauthlib>=0.4.6',
        'google-auth-httplib2>=0.1.0',
        'google-api-python-client>=2.0.0',
        'Pillow>=10.0.0'
    ],
    entry_points={
        'console_scripts': [
            'gs-browser=gs_browser:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern web browser with Google integration",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gs-browser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={
        'gs_browser': [
            'icons/*.png',
            'config/*.json',
            '*.html',
            '*.qss'
        ],
    },
) 