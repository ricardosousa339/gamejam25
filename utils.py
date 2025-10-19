"""
Utility functions for the game
"""
import os
import sys


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    
    When PyInstaller bundles the app, it creates a temporary folder
    and stores path in _MEIPASS. This function resolves the correct path
    whether running from source or as a bundled executable.
    
    Args:
        relative_path (str): Relative path to the resource
        
    Returns:
        str: Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running from source, use current directory
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
