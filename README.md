# 🐍 Python Portfolio

<div align="center">

```
    ____        __  __                   ____            __  ____      ___    
   / __ \__  __/ /_/ /_  ____  ____    / __ \____  ____/ /_/ __/___  / (_)___
  / /_/ / / / / __/ __ \/ __ \/ __ \  / /_/ / __ \/ ___/ __/ /_/ __ \/ / / __ \
 / ____/ /_/ / /_/ / / / /_/ / / / / / ____/ /_/ / /  / /_/ __/ /_/ / / / /_/ /
/_/    \__, /\__/_/ /_/\____/_/ /_/ /_/    \____/_/   \__/_/  \____/_/_/\____/ 
      /____/                                                                   
```

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GUI](https://img.shields.io/badge/GUI-tkinter-orange.svg)
![AI](https://img.shields.io/badge/AI-OpenAI-purple.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

**🚀 Modern Desktop Applications with AI Integration**

[View Projects](#-featured-projects) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

## 📋 Table of Contents

- [About](#-about)
- [Featured Projects](#-featured-projects)
  - [ASCII Art Generator](#-ascii-art-generator)
  - [Mr. CleanData](#-mr-cleandata)
  - [PlotIQ](#-plotiq)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)

- [API Setup](#-api-setup)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🎯 About

This repository showcases my Python development skills through three comprehensive desktop applications. Each project demonstrates different aspects of modern software development including GUI design, AI integration, data processing, and user experience optimization.

> **⭐ If you find these projects useful, please consider giving this repository a star!**

## 🚀 Featured Projects

### 🎨 ASCII Art Generator
**[`source code/ASCII Art Generator.py`](./source%20code/ASCII%20Art%20Generator.py)**

Transform images and GIFs into animated ASCII art with procedural effects.

<details>
<summary>🔍 View Features</summary>

```
📷 Image Input → 🎭 ASCII Conversion → ✨ Animation → 💾 Export
```

**Core Features:**
- ✅ Multi-format support (JPG, PNG, BMP, GIF)
- ✅ Animated GIF processing with frame extraction
- ✅ 6 procedural animation effects (wave, flicker, glitch, rain, morph, cycle)
- ✅ Real-time animation controls and frame navigation
- ✅ Customizable ASCII character sets
- ✅ Batch export and clipboard integration

**Technical Implementation:**
- Custom tkinter GUI with modern dark theme
- PIL/Pillow for advanced image processing
- Multi-threaded animation rendering
- Efficient memory management for large GIFs

</details>

---

### 🧽 Mr. CleanData
**[`source code/Dataset Cleaner.py`](./source%20code/Dataset%20Cleaner.py)**

AI-powered dataset analysis and cleaning tool with OpenAI integration.

<details>
<summary>🔍 View Features</summary>

```
📊 Data Input → 🤖 AI Analysis → 🧹 Smart Cleaning → 📈 Export
```

**Core Features:**
- ✅ OpenAI GPT-3.5 integration for intelligent analysis
- ✅ Support for CSV, Excel, JSON, TSV formats
- ✅ Automated issue detection (missing values, duplicates, outliers)
- ✅ Smart cleaning recommendations with priority levels
- ✅ Real-time progress tracking and detailed logging
- ✅ Fallback analysis when AI is unavailable

**Technical Implementation:**
- RESTful API integration with error handling
- Pandas-powered data manipulation
- Threaded processing for responsive UI
- JSON-based AI communication protocol

</details>

---

### 📈 PlotIQ
**[`source code/Plot Generator.py`](./source%20code/Plot%20Generator.py)**

Natural language to data visualization converter using AI.

<details>
<summary>🔍 View Features</summary>

```
💬 Natural Language → 🤖 Code Generation → 📊 Visualization
```

**Core Features:**
- ✅ Natural language plot descriptions
- ✅ Automatic Python code generation
- ✅ Matplotlib & Seaborn integration
- ✅ Interactive data preview and statistics
- ✅ Dark theme optimized visualizations
- ✅ Multi-format data loading

**Technical Implementation:**
- OpenAI API for code generation
- Dynamic Python code execution
- Matplotlib backend integration
- Comprehensive error handling and validation

</details>

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **GUI Framework** | `tkinter` • `ttk` |
| **AI Integration** | `OpenAI API` • `GPT-3.5-turbo` |
| **Data Processing** | `pandas` • `numpy` |
| **Visualization** | `matplotlib` • `seaborn` |
| **Image Processing** | `PIL/Pillow` |
| **Networking** | `requests` |

</div>

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Clone Repository
```bash
git clone https://github.com/treblalbert/Python-Projects.git
cd Python-Projects
```

### Install Dependencies
```bash
pip install tkinter pillow pandas numpy matplotlib seaborn openai requests pathlib
```

### Project Structure
```
Python-Projects/
├── README.md
├── requirements.txt
├── LICENSE
└── source code/
    ├── ASCII Art Generator.py
    ├── Dataset Cleaner.py
    └── Plot Generator.py
```

### Alternative: Requirements File
```bash
pip install -r requirements.txt
```

<details>
<summary>📄 requirements.txt</summary>

```
Pillow>=9.0.0
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0
openai>=1.0.0
requests>=2.28.0
pathlib2>=2.3.0
```

</details>

## 🚀 Usage

### Running Applications
```bash
# Navigate to source code directory
cd "source code"

# ASCII Art Generator
python "ASCII Art Generator.py"

# Dataset Cleaner
python "Dataset Cleaner.py"

# Plot Generator
python "Plot Generator.py"
```

### Basic Workflow
1. **Launch** any application
2. **Configure** API key (for AI-powered tools)
3. **Load** your data/image
4. **Process** with AI assistance
5. **Export** results

## 🔑 API Setup

### OpenAI Configuration
1. **Get API Key**: Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Set in Application**: Enter key in the setup tab of AI-powered tools
3. **Start Processing**: Begin using intelligent features

### Supported Models
- ✅ GPT-3.5-turbo (recommended)
- ✅ GPT-4 (premium features)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **🍴 Fork** the repository
2. **🌟 Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **💾 Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **📤 Push** to the branch (`git push origin feature/AmazingFeature`)
5. **🔄 Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Include error handling
- Test on multiple Python versions
- Update documentation

**See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.**

## 📊 Repository Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/treblalbert/Python-Projects?style=social)
![GitHub forks](https://img.shields.io/github/forks/treblalbert/Python-Projects?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/treblalbert/Python-Projects?style=social)

</div>

## 📄 License

This project is licensed under the **MIT License** - see the [`LICENSE`](LICENSE) file for details.

## 📞 Contact

<div align="center">

**Let's Connect!**

[![GitHub](https://img.shields.io/badge/GitHub-treblalbert-181717?style=for-the-badge&logo=github)](https://github.com/treblalbert)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-albert--adroer--prats-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/albert-adroer-prats-615388160/)
[![Email](https://img.shields.io/badge/Email-albertadroer@gmail.com-D14836?style=for-the-badge&logo=gmail)](mailto:albertadroer@gmail.com)

</div>

---

<div align="center">

**🌟 Star this repository if you found it helpful! 🌟**

```
  ╔══════════════════════════════════════════════════════════╗
  ║  Thanks for visiting my Python Portfolio! 🐍            ║
  ║  Feel free to explore, fork, and contribute! 🚀         ║
  ╚══════════════════════════════════════════════════════════╝
```

**Made with ❤️ and lots of ☕**

</div>
