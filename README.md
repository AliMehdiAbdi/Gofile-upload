# 📤 Gofile Upload

A modern terminal-based file uploader for [Gofile.io](https://gofile.io) with progress tracking and beautiful output.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Features

- 🚀 **Fast Uploads** with progress tracking
- 📊 **Beautiful Terminal UI** powered by Rich
- 📁 **Recursive Folder Uploads**
- 🔑 **API Key Support** via `.env` file
- 🛠 **Error Handling** with clean error messages
- ⚡ **Real-time Stats** (Speed, Time Remaining, Progress)

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/gofile-uploader.git
cd gofile-uploader
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Upload
```bash
python gofile_uploader.py file.txt
```

### Upload Multiple Files/Folders
```bash
python gofile_uploader.py file1.txt file2.txt my_folder/
```

## ⚙️ Configuration

Create `.env` file:
```env
GOFILE_API_KEY=your_api_key_here
```

## 🛠 Development

1. **Setup virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

## 🤝 Contributing

Contributions welcome! Please follow these steps:
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

Made with ❤️ by **Ali Mehdi** • [![GitHub](https://img.shields.io/badge/GitHub-Profile-blue)](https://github.com/AliMehdiAbdi)
