# VisionSpeak - Installation Guide

This guide provides detailed installation instructions for VisionSpeak on various operating systems.

## Table of Contents

- [System Requirements](#system-requirements)
- [Python Installation](#python-installation)
- [Tesseract OCR Installation](#tesseract-ocr-installation)
  - [macOS](#macos)
  - [Ubuntu/Debian Linux](#ubuntudebian-linux)
  - [Windows](#windows)
- [Python Dependencies](#python-dependencies)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

- **Operating System**: macOS 10.14+, Windows 10+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Disk Space**: At least 500 MB free space
- **Display**: 1280x800 or higher resolution

## Python Installation

### Check if Python is Already Installed

Open a terminal/command prompt and run:

```bash
python --version
# or
python3 --version
```

If Python 3.8+ is installed, you can proceed to the next section.

### Install Python (if needed)

#### macOS

```bash
# Using Homebrew
brew install python3
```

Or download from [python.org](https://www.python.org/downloads/)

#### Ubuntu/Debian Linux

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk
```

#### Windows

Download the installer from [python.org](https://www.python.org/downloads/)

- Make sure to check "Add Python to PATH" during installation
- Install pip (usually included with Python 3.4+)

## Tesseract OCR Installation

Tesseract OCR Engine must be installed separately as it's a system-level application.

### macOS

#### Option 1: Using Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Tesseract
brew install tesseract

# Optional: Install additional language packs
brew install tesseract-lang
```

#### Option 2: Using MacPorts

```bash
sudo port install tesseract
```

#### Verify Installation

```bash
tesseract --version
```

### Ubuntu/Debian Linux

```bash
# Update package list
sudo apt-get update

# Install Tesseract OCR
sudo apt-get install tesseract-ocr

# Install language data (optional)
sudo apt-get install tesseract-ocr-eng  # English (installed by default)
sudo apt-get install tesseract-ocr-fra  # French
sudo apt-get install tesseract-ocr-spa  # Spanish
sudo apt-get install tesseract-ocr-deu  # German
# Add more languages as needed
```

#### Verify Installation

```bash
tesseract --version
```

### Fedora/RHEL/CentOS

```bash
# Install Tesseract
sudo dnf install tesseract

# Or using yum
sudo yum install tesseract
```

### Windows

#### Option 1: Using Installer (Recommended)

1. **Download Tesseract Installer**

   - Go to [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
   - Download the latest installer (e.g., `tesseract-ocr-w64-setup-v5.3.3.20231005.exe`)

2. **Run the Installer**

   - Execute the downloaded file
   - Follow the installation wizard
   - Note the installation path (usually `C:\Program Files\Tesseract-OCR`)
   - Make sure to install English language data

3. **Add Tesseract to PATH**

   - Open "System Properties" → "Environment Variables"
   - Under "System variables", find and edit "Path"
   - Add the Tesseract installation directory (e.g., `C:\Program Files\Tesseract-OCR`)
   - Click "OK" to save

4. **Verify Installation**
   Open Command Prompt and run:
   ```cmd
   tesseract --version
   ```

#### Option 2: Using Chocolatey

```powershell
# Install Chocolatey if not installed
# Then:
choco install tesseract

# Verify
tesseract --version
```

#### Manual Path Configuration (if needed)

If Tesseract is not found after installation, you may need to set the path manually in the code:

Edit `ocr_engine.py` and add the following in the `__init__` method:

```python
# For Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Python Dependencies

### Install Required Python Packages

1. **Navigate to the project directory**

   ```bash
   cd /path/to/IPV-project
   ```

2. **Install dependencies using pip**

   ```bash
   pip install -r requirements.txt
   ```

   Or using pip3:

   ```bash
   pip3 install -r requirements.txt
   ```

### Manual Installation (Alternative)

If you prefer to install packages individually:

```bash
# Image processing
pip install opencv-python==4.8.1.78
pip install Pillow==10.1.0
pip install numpy==1.26.2

# OCR
pip install pytesseract==0.3.10

# Text-to-Speech
pip install pyttsx3==2.90
```

### Virtual Environment (Recommended)

Using a virtual environment helps avoid conflicts with other Python projects:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Verification

### Test Tesseract Installation

Create a test script `test_tesseract.py`:

```python
import pytesseract
from PIL import Image

print("Tesseract Version:", pytesseract.get_tesseract_version())
print("Available Languages:", pytesseract.get_languages())
```

Run it:

```bash
python test_tesseract.py
```

Expected output:

```
Tesseract Version: 5.x.x
Available Languages: ['eng', 'osd']
```

### Test Image Processing

Create a test script `test_opencv.py`:

```python
import cv2
import numpy as np
from PIL import Image

print("OpenCV Version:", cv2.__version__)
print("NumPy Version:", np.__version__)
print("Pillow Version:", Image.__version__)
print("All packages loaded successfully!")
```

Run it:

```bash
python test_opencv.py
```

### Test Text-to-Speech

Create a test script `test_tts.py`:

```python
import pyttsx3

engine = pyttsx3.init()
print("TTS Engine initialized successfully!")
print("Available voices:", len(engine.getProperty('voices')))
engine.say("VisionSpeak is ready to use!")
engine.runAndWait()
```

Run it:

```bash
python test_tts.py
```

You should hear the spoken message.

## Troubleshooting

### Issue: "pytesseract.pytesseract.TesseractNotFoundError"

**Solution**:

1. Verify Tesseract is installed: `tesseract --version`
2. Ensure Tesseract is in your system PATH
3. On Windows, manually set the path in `ocr_engine.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Issue: "ModuleNotFoundError: No module named 'cv2'"

**Solution**:

```bash
pip install opencv-python
```

### Issue: "ModuleNotFoundError: No module named 'PIL'"

**Solution**:

```bash
pip install Pillow
```

### Issue: "ImportError: cannot import name '\_imaging'"

**Solution**:
Pillow installation issue. Reinstall:

```bash
pip uninstall Pillow
pip install Pillow
```

### Issue: TTS not working on Linux

**Solution**:
Install espeak:

```bash
sudo apt-get install espeak
```

### Issue: Permission denied on macOS

**Solution**:
Use pip with --user flag:

```bash
pip install --user -r requirements.txt
```

### Issue: Multiple Python versions causing conflicts

**Solution**:
Use virtual environment (recommended) or specify Python version explicitly:

```bash
python3.8 -m pip install -r requirements.txt
python3.8 gui.py
```

### Issue: Tkinter not found

**Solution**:

**Ubuntu/Debian**:

```bash
sudo apt-get install python3-tk
```

**macOS** (usually included with Python):

```bash
brew install python-tk
```

**Windows**: Reinstall Python and ensure "tcl/tk and IDLE" is checked during installation.

## Additional Language Packs (Optional)

To recognize text in languages other than English, install additional Tesseract language packs:

### macOS

```bash
brew install tesseract-lang
```

### Ubuntu/Debian

```bash
# List available languages
apt-cache search tesseract-ocr

# Install specific languages
sudo apt-get install tesseract-ocr-fra  # French
sudo apt-get install tesseract-ocr-spa  # Spanish
sudo apt-get install tesseract-ocr-deu  # German
sudo apt-get install tesseract-ocr-chi-sim  # Simplified Chinese
```

### Windows

During Tesseract installation, select additional language packs, or download them separately from the [Tesseract GitHub repository](https://github.com/tesseract-ocr/tessdata).

## Running the Application

Once everything is installed:

```bash
# Navigate to project directory
cd /path/to/IPV-project

# Run the application
python gui.py
# or
python3 gui.py
```

If using a virtual environment:

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Then run
python gui.py
```

## Performance Optimization

### For Large Images

If processing large images is slow, consider:

1. **Resize images** before processing (done automatically in the app)
2. **Use SSD storage** for faster I/O
3. **Increase available RAM**

### For Better OCR Accuracy

1. **Install high-quality language data**:

   ```bash
   # Download best quality data
   wget https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata
   # Place in Tesseract data directory
   ```

2. **Use appropriate PSM modes** based on document layout

## Getting Help

If you encounter issues not covered here:

1. Check the [README.md](README.md) for common solutions
2. Verify all dependencies are correctly installed
3. Check Tesseract and Python versions
4. Open an issue on the project repository with:
   - Your operating system and version
   - Python version (`python --version`)
   - Tesseract version (`tesseract --version`)
   - Complete error message
   - Steps to reproduce the issue

---

**Happy OCR-ing with VisionSpeak!** 🚀
