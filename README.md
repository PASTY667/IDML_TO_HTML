# IDML to HTML Converter

A Python tool for converting Adobe InDesign IDML files into HTML email signatures.

## 📋 Description

This project extracts and parses IDML (InDesign Markup Language) files to generate HTML/CSS output. It processes spreads, stories, and styles from InDesign documents to create web-ready signatures.

## 🚀 Features

- ✅ Extract IDML files (ZIP archives)
- ✅ Parse spreads with support for TextFrames, Rectangles, and Images
- ✅ Geometric bounds detection and conversion
- ✅ JSON preview generation for debugging
- 🚧 Story parsing (in development)
- 🚧 Style parsing (in development)
- 🚧 HTML/CSS generation (in development)

## 📦 Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/PASTY667/idml-to-html.git
cd idml-to-html
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create required directories:
```bash
mkdir -p idml_input temp html_output
```

## 💻 Usage

### Basic Usage

Place your InDesign file named `signature.idml` in the `idml_input/` folder, then run:

```bash
python main.py
```

### Command Line Options

```bash
python main.py [OPTIONS]
```

#### Available Options

| Option | Short | Description |
|--------|-------|-------------|
| `--clear-temp` | `-ct` | Clear temporary folder after execution |

#### Examples

```bash
# Run with temp folder cleanup
python main.py --clear-temp

# Run with temp folder cleanup (short form)
python main.py -ct
```

## 📁 Project Structure

```
.
├── idml_input/           # Input folder for IDML files
│   └── signature.idml    # Your InDesign file (required)
├── idml_parser/          # Core parsing modules
│   ├── extract.py        # IDML extraction (unzip)
│   ├── spreads.py        # Spread parsing
│   ├── stories.py        # Story parsing (TODO)
│   ├── styles.py         # Style parsing (TODO)
│   └── builder.py        # HTML generation (TODO)
├── html_output/          # Generated HTML output
├── temp/                 # Temporary extraction folder
│   └── spreads_preview.json  # Debug preview
├── main.py               # Entry point
├── clear_temp.py         # Temp folder utilities
└── requirements.txt      # Python dependencies
```

## 🔍 Output

The tool generates:
- **`temp/spreads_preview.json`**: JSON representation of parsed spreads for debugging
- **`idml_to_html.log`**: Detailed execution log
- **`html_output/`**: Final HTML/CSS files (when implemented)

### Example Log Output

```
2025-10-27 21:10:47,081 - INFO - Checking output folder
2025-10-27 21:10:47,081 - INFO - Output folder exists
2025-10-27 21:10:47,090 - INFO - Extraction successful
2025-10-27 21:10:47,093 - INFO - Parsed spread Spread_ueb with 12 elements.
2025-10-27 21:10:47,093 - INFO - Spread Spread_ueb parsed successfully: 11 TextFrames, 1 Rectangles, 0 Images.
```

## 🛠️ Development Status

### ✅ Implemented
- IDML extraction with error handling
- Spread parsing with geometric bounds
- TextFrame, Rectangle, and Image detection
- JSON preview generation
- Logging system

### 🚧 In Progress
- Story content parsing
- Style sheet parsing
- HTML/CSS generation
- Template system

## 📝 Dependencies

- **Jinja2**: Template engine for HTML generation
- **lxml**: XML processing
- **beautifulsoup4**: HTML parsing and manipulation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**PASTY667**

## 🐛 Known Issues

- Some elements may not have GeometricBounds attributes (logged as warnings)
- Story and style parsing not yet implemented
- HTML output generation pending

## 📮 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.