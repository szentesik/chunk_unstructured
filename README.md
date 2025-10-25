# PDF Document Processing with Unstructured

A Python application for high-resolution PDF document processing using the Unstructured library. This tool extracts text, images, and tables from PDF documents with OCR capabilities.

## Features

- 🔍 **High-resolution PDF processing** with OCR text recognition
- 🖼️ **Image extraction** from PDF documents
- 📊 **Table extraction** and processing
- 🌐 **Multi-language support** (currently configured for English)
- 📈 **Progress tracking** with visual progress bars
- ⚡ **Batch processing** of multiple PDF files

## Prerequisites

Before installing the Python dependencies, you need to install the following system-level applications:

### 1. Tesseract OCR

Tesseract is required for OCR (Optical Character Recognition) functionality.

#### Windows
1. Download the Windows installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and follow the setup wizard
3. Add the Tesseract installation folder to your system PATH:
   - Open System Properties → Environment Variables
   - Add `C:\Program Files\Tesseract-OCR` to your PATH variable
4. Verify installation by opening Command Prompt and running: `tesseract --version`

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr
```

### 2. Poppler

Poppler is required for PDF to image conversion.

#### Windows
1. Download Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract the downloaded zip file to a folder (e.g., `C:\Program Files\poppler-25.07.0`)
3. Add the `Library\bin` folder to your system PATH:
   - Open System Properties → Environment Variables
   - Add `C:\Program Files\poppler-25.07.0\Library\bin` to your PATH variable
4. Verify installation by opening Command Prompt and running: `pdftoppm -h`

#### macOS
```bash
brew install poppler
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install poppler-utils
```

## Installation

### 1. Clone or Download the Project

```bash
git clone https://github.com/szentesik/chunk_unstructured.git
cd chunk_unstructured
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

#### Windows
```bash
.venv\Scripts\activate
```

#### macOS/Linux
```bash
source .venv/bin/activate
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- `unstructured[pdf,local-inference]` - Main PDF processing library
- `pdf2image` - PDF to image conversion
- `pytesseract` - Python wrapper for Tesseract
- `tesseract` - Tesseract OCR engine
- `poppler-utils` - Poppler utilities
- `huggingface_hub[hf_xet]` - Hugging Face Hub Xet Storage support
- `tiktoken` - Fast BPE tokenizer for OpenAI models
- `python-dotenv` - Load environment from .env files

## Usage

### Basic Usage

1. Place your PDF files in the `../data` directory (relative to the script)
2. Run the application:

```bash
python chunk.py
```

### Configuration

The application processes all PDF files in the specified directory with the following settings:

- **Strategy**: High-resolution processing (`hi_res`)
- **Language**: English (`eng`)
- **Image Extraction**: Enabled
- **Table Extraction**: Enabled
- **Image Payload**: Enabled

### Output

The application will:
1. Display a progress bar while processing files
2. Show processing status for each file
3. Extract and return structured elements from PDFs
4. Display the total number of elements extracted

## Project Structure

```
chunk_unstructured/
├── chunk.py              # Main application script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .venv/               # Virtual environment (created during setup)
└── ../data/             # Directory containing PDF files to process
```

## Troubleshooting

### Common Issues

#### "tesseract is not installed or it's not in your PATH"
- **Solution**: Ensure Tesseract is installed and added to your system PATH
- **Verification**: Run `tesseract --version` in Command Prompt/Terminal

#### "Unable to get page count. Is poppler installed and in PATH?"
- **Solution**: Ensure Poppler is installed and added to your system PATH
- **Verification**: Run `pdftoppm -h` in Command Prompt/Terminal

#### Unicode encoding errors on Windows
- **Solution**: The script automatically handles UTF-8 encoding on Windows
- **Note**: This is already configured in the code

### Performance Notes

- High-resolution processing takes longer but provides better results
- Processing time depends on PDF complexity and size
- Typical processing time: 10-30 seconds per PDF file

## Dependencies

### Python Packages
- `unstructured[pdf,local-inference]>=0.18.15` - Core PDF processing
- `pdf2image>=1.17.0` - PDF to image conversion
- `pytesseract>=0.3.13` - Tesseract Python wrapper
- `tesseract>=0.1.3` - Tesseract OCR engine
- `poppler-utils>=0.1.0` - Poppler utilities
- `huggingface_hub[hf_xet]>=0.36.0` - Hugging Face Hub Xet Storage support
- `tiktoken>=0.8.0` - Fast BPE tokenizer for OpenAI models (for token count estimation)
- `python-dotenv>=1.1.1` - Load environment from .env files

### System Requirements
- Python 3.8 or higher
- Tesseract OCR (system installation)
- Poppler (system installation)
- Sufficient RAM for image processing (recommended: 4GB+)

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Verify all system dependencies are installed correctly
3. Ensure your virtual environment is activated
4. Check that PDF files are in the correct directory
