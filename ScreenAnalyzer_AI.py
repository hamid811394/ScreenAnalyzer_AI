import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import json
from datetime import datetime
from pynput import keyboard
from PIL import ImageGrab
import pytesseract
import google.generativeai as genai
import ctypes
import sys

# <CHANGE> Add your API key here manually
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

class ScreenAnalyzerApp:
    def __init__(self):
        self.overlay_visible = False
        self.overlay_window = None
        
        # <CHANGE> Use the hardcoded API key instead of loading from config
        self.api_key = GEMINI_API_KEY
        
        # Configure Gemini API
        if self.api_key and self.api_key != "YOUR_API_KEY_HERE":
            genai.configure(api_key=self.api_key)
        
        # Create overlay window (hidden initially)
        self.create_overlay()
        
        # Start listening for hotkeys
        self.start_hotkey_listener()

    def create_overlay(self):
        """Create the overlay window"""
        if self.overlay_window is not None:
            return

        self.overlay_window = tk.Tk()
        self.overlay_window.title("Screen Analyzer AI")
        self.overlay_window.geometry("600x500+100+50")

        # <CHANGE> Enhanced window layering for Windows
        if sys.platform == 'win32':
            # Set as always on top
            self.overlay_window.attributes('-topmost', True)
            # Remove from taskbar
            self.overlay_window.attributes('-toolwindow', True)
            # Make it a layered window to overlay on everything
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd != 0:
                ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 3)
        else:
            # For non-Windows systems
            self.overlay_window.attributes('-topmost', True)

        # Set background color
        self.overlay_window.configure(bg='#1e1e1e')

        # <CHANGE> Removed API Key Section entirely
        
        # Question Container
        question_label = tk.Label(self.overlay_window, text="Question (Editable):", fg='#ffffff', bg='#1e1e1e', font=('Arial', 10, 'bold'))
        question_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

        self.question_text = scrolledtext.ScrolledText(
            self.overlay_window,
            height=6,
            width=70,
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='white',
            wrap=tk.WORD
        )
        self.question_text.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=False)

        # Response Container
        response_label = tk.Label(self.overlay_window, text="Answer:", fg='#ffffff', bg='#1e1e1e', font=('Arial', 10, 'bold'))
        response_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

        self.response_text = scrolledtext.ScrolledText(
            self.overlay_window,
            height=8,
            width=70,
            bg='#3d3d3d',
            fg='#90ee90',
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.response_text.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        # Status Bar
        self.status_label = tk.Label(self.overlay_window, text="Ready | Press '.1' to capture | '.3' to toggle", fg='#90ee90', bg='#1e1e1e', font=('Arial', 8))
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        # Hide window initially
        self.overlay_window.withdraw()

        # Prevent window from closing on X button click
        self.overlay_window.protocol("WM_DELETE_WINDOW", self.toggle_overlay)

    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.overlay_window.update()

    def toggle_overlay(self):
        """Toggle overlay visibility"""
        self.overlay_visible = not self.overlay_visible

        if self.overlay_visible:
            self.overlay_window.deiconify()
            self.overlay_window.lift()
            # <CHANGE> Force window to top on every toggle
            self.overlay_window.attributes('-topmost', True)
            self.update_status("Window visible | Press '.3' to hide")
        else:
            self.overlay_window.withdraw()
            self.update_status("Window hidden")

    def capture_and_analyze(self):
        """Capture screenshot and extract text"""
        try:
            self.update_status("Capturing screenshot...")

            # Capture screenshot
            screenshot = ImageGrab.grab()

            # Extract text using Tesseract
            self.update_status("Extracting text from screenshot...")
            text = pytesseract.image_to_string(screenshot)

            if not text.strip():
                self.update_status("No text found in screenshot")
                return

            # Show overlay and display question
            if not self.overlay_visible:
                self.toggle_overlay()

            self.question_text.config(state=tk.NORMAL)
            self.question_text.delete(1.0, tk.END)
            self.question_text.insert(1.0, text)
            self.question_text.config(state=tk.NORMAL)

            self.update_status("Text extracted. Analyzing with Gemini...")

            # Get answer from Gemini in a separate thread
            threading.Thread(target=self.get_gemini_answer, daemon=True).start()

        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    def get_gemini_answer(self):
        """Get answer from Gemini API"""
        try:
            if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
                self.update_status("Error: API key not configured")
                return

            question = self.question_text.get(1.0, tk.END).strip()

            if not question:
                self.update_status("Error: No question text")
                return

            # Create prompt
            prompt = f"""You are a helpful AI assistant. The following text was extracted from a screenshot of a question/problem. Please analyze it and provide a clear, concise answer:

QUESTION:
{question}

Please provide a direct and helpful answer."""

            # Call Gemini API
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)

            # Display response
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(1.0, response.text)
            self.response_text.config(state=tk.DISABLED)

            self.update_status("Answer generated successfully!")

        except Exception as e:
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(1.0, f"Error getting answer: {str(e)}")
            self.response_text.config(state=tk.DISABLED)
            self.update_status(f"Error: {str(e)}")

    def on_press(self, key):
        """Handle key press events"""
        try:
            # Check for '.1' (period and 1)
            if hasattr(key, 'char'):
                if key.char == '.':
                    self.last_dot_time = datetime.now()
                elif key.char == '1':
                    # Check if this is within 0.5 seconds of a dot
                    if hasattr(self, 'last_dot_time'):
                        time_diff = (datetime.now() - self.last_dot_time).total_seconds()
                        if time_diff < 0.5:
                            threading.Thread(target=self.capture_and_analyze, daemon=True).start()

                elif key.char == '3':
                    # Check if this is within 0.5 seconds of a dot
                    if hasattr(self, 'last_dot_time'):
                        time_diff = (datetime.now() - self.last_dot_time).total_seconds()
                        if time_diff < 0.5:
                            self.toggle_overlay()

        except AttributeError:
            pass

    def start_hotkey_listener(self):
        """Start listening for hotkeys"""
        listener = keyboard.Listener(on_press=self.on_press)
        listener.daemon = True
        listener.start()

    def run(self):
        """Start the application"""
        self.overlay_window.mainloop()


if __name__ == "__main__":
    app = ScreenAnalyzerApp()
    app.run()
