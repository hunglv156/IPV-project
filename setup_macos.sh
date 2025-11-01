#!/bin/bash

# VisionSpeak Setup Script for macOS
# Tự động cài đặt tất cả dependencies

set -e  # Exit on error

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         🚀 VisionSpeak Setup for macOS 🚀                ║"
echo "║    Adaptive OCR & TTS with Vietnamese Support            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is for macOS only!"
    exit 1
fi

print_info "Checking system requirements..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    print_error "Homebrew is not installed!"
    echo "Please install Homebrew first:"
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
else
    print_success "Homebrew is installed"
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Installing Python 3..."
    brew install python@3.13
else
    PYTHON_VERSION=$(python3 --version)
    print_success "Python is installed: $PYTHON_VERSION"
fi

# Install Tesseract if not installed
echo ""
print_info "Checking Tesseract OCR..."
if ! command -v tesseract &> /dev/null; then
    print_info "Installing Tesseract OCR..."
    brew install tesseract tesseract-lang
    print_success "Tesseract installed successfully"
else
    TESSERACT_VERSION=$(tesseract --version | head -n 1)
    print_success "Tesseract is already installed: $TESSERACT_VERSION"
    
    # Check if Vietnamese language pack is installed
    if tesseract --list-langs 2>&1 | grep -q "vie"; then
        print_success "Vietnamese language pack is installed"
    else
        print_info "Installing Vietnamese language pack..."
        brew install tesseract-lang
        print_success "Vietnamese language pack installed"
    fi
fi

# Create virtual environment
echo ""
print_info "Setting up Python virtual environment..."
if [ -d "venv" ]; then
    print_info "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
print_success "Virtual environment created"

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Verify we're in venv
if [[ "$VIRTUAL_ENV" != "" ]]; then
    print_success "Virtual environment activated: $VIRTUAL_ENV"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo ""
print_info "Upgrading pip..."
python -m pip install --upgrade pip --quiet
print_success "pip upgraded"

# Install Python packages
echo ""
print_info "Installing Python packages (this may take a few minutes)..."
echo ""

# Install packages one by one to better track progress
packages=(
    "numpy"
    "Pillow"
    "opencv-python"
    "pytesseract"
    "pyttsx3"
    "gTTS"
    "pygame"
    "langdetect"
)

for package in "${packages[@]}"; do
    print_info "Installing $package..."
    if pip install "$package" --quiet; then
        print_success "$package installed"
    else
        print_error "Failed to install $package"
        echo "Trying alternative method..."
        pip install "$package" --no-cache-dir
    fi
done

# Verify installations
echo ""
print_info "Verifying installations..."

python -c "
import sys
errors = []

packages = {
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'numpy': 'numpy',
    'pytesseract': 'pytesseract',
    'pyttsx3': 'pyttsx3',
    'gtts': 'gTTS',
    'pygame': 'pygame',
    'langdetect': 'langdetect'
}

for module, package in packages.items():
    try:
        __import__(module)
        print(f'✅ {package}')
    except ImportError as e:
        errors.append(f'{package}: {e}')
        print(f'❌ {package}')

if errors:
    print('\n❌ Some packages failed to import:')
    for error in errors:
        print(f'  - {error}')
    sys.exit(1)
else:
    print('\n✅ All packages imported successfully!')
"

if [ $? -eq 0 ]; then
    print_success "All Python packages verified"
else
    print_error "Some packages failed verification"
    echo ""
    echo "You can try installing failed packages manually:"
    echo "  source venv/bin/activate"
    echo "  pip install <package-name>"
    exit 1
fi

# Run Vietnamese support test
echo ""
print_info "Running Vietnamese support test..."
if [ -f "test_vietnamese.py" ]; then
    python test_vietnamese.py
else
    print_info "test_vietnamese.py not found, skipping test"
fi

# Create convenience scripts
echo ""
print_info "Creating convenience scripts..."

# Create run script
cat > run_app.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python gui.py
EOF
chmod +x run_app.sh
print_success "Created run_app.sh"

# Create test script
cat > run_test.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python test_vietnamese.py
EOF
chmod +x run_test.sh
print_success "Created run_test.sh"

# Summary
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              🎉 Setup Complete! 🎉                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
print_success "VisionSpeak is ready to use!"
echo ""
echo "📋 Next steps:"
echo ""
echo "  1️⃣  To run the application:"
echo "     ${GREEN}./run_app.sh${NC}"
echo "     or manually:"
echo "     ${GREEN}source venv/bin/activate && python gui.py${NC}"
echo ""
echo "  2️⃣  To test Vietnamese support:"
echo "     ${GREEN}./run_test.sh${NC}"
echo ""
echo "  3️⃣  To use from code:"
echo "     ${GREEN}source venv/bin/activate && python${NC}"
echo ""
echo "📚 Documentation:"
echo "  - README.md - Project overview"
echo "  - VIETNAMESE_SUPPORT.md - Vietnamese features"
echo "  - SETUP_MACOS.md - Detailed setup guide"
echo ""
echo "💡 Tip: Add this to your ~/.zshrc for quick access:"
echo "     ${GREEN}alias visionspeak='cd $(pwd) && ./run_app.sh'${NC}"
echo ""
print_success "Happy OCR & TTS! 🚀"
echo ""

