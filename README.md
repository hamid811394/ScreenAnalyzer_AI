# ScreenAnalyzer_AI

ScreenAnalyzer_AI is a lightweight desktop tool that captures text from your screen using OCR and analyzes it using Gemini AI to provide clear and instant answers. With keyboard-triggered automation, screenshot-to-text extraction, a clean overlay interface, and AI-powered response generation, the tool makes studying, research, and question answering faster and more convenient — without typing anything manually.

---

## 🚀 Features

- ✔️ Global keyboard trigger for screen capture  
- ✔️ OCR-based text extraction using Tesseract  
- ✔️ Gemini AI-powered answer generation  
- ✔️ Lightweight always-on-top overlay UI  
- ✔️ Editable detected text before generating output  
- ✔️ Background listener (runs silently until triggered)  
- ✔️ Converts easily to `.exe` for Windows

---

## 📦 Installation

Clone the repository:

git clone https://github.com/hamid811394/ScreenAnalyzer_AI.git

Python 3.8+ recommended.

Install the dependencies:
pip install -r requirements.txt

Tesseract OCR must also be installed separately and added to PATH.
Install Tesseract OCR

To enable text extraction, you must install Tesseract OCR manually (it is not included in Python modules).

1️⃣ Download Tesseract

You can download the official Windows installer from the project’s GitHub releases page:

👉 https://github.com/tesseract-ocr/tesseract/releases
Add Tesseract to System Environment Variables (If Needed)
Step-by-step

1. Open Windows Search → type Environment Variables
2. Click "Edit the system environment variables"
3. Click "Environment Variables…"
4. Under System variables, find and select:
5. Path → click Edit
6. Click New and paste the Tesseract installation path: "C:\Program Files\Tesseract-OCR\"
7. Click OK to save and exit.

🧪 Verify Installation

Open Command Prompt and type:

tesseract --version

▶️ Running the Application

Run the tool using:

python screen_analyzer.py

🎯 Keyboard Shortcuts
Shortcut	Action
.1 (dot + 1 quickly)	Capture screen → extract text → send to AI...
.3 (dot + 3 quickly)	Show / Hide the overlay window...

🧠 AI Configuration

Inside the script, update your Gemini API key:
GEMINI_API_KEY = "YOUR_API_KEY"


🖥️ Convert to EXE (Windows)

Use PyInstaller to generate a standalone executable:
Open CMD in the same Folder and past it  "pyinstaller -F -w -i icon.ico screen_analyzer.py"
-F → single file EXE
-w → hides console
-i icon.ico → optional custom icon

After completion, your .exe file will be located in:
dist/




