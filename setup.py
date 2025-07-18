from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'packages': ['rumps', 'dotenv', 'supabase', 'os', 'webbrowser','AppKit', 'datetime', 'dateutil.parser'],
    'resources': ['.env'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)