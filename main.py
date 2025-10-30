"""
VisionSpeak - Main Entry Point
Launches the VisionSpeak GUI application
"""

import sys
import tkinter as tk
from gui import VisionSpeakApp


def main():
    """
    Main entry point for the VisionSpeak application.
    Creates and runs the GUI.
    """
    # Create root window
    root = tk.Tk()
    
    # Create application instance
    app = VisionSpeakApp(root)
    
    # Start the main event loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

