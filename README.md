# 🤖 Sofware-AI

An intelligent assistant for Windows OS with a graphical user interface and full support for Persian language.

## ✨ Features

- 🎯 Modern Gemini-like GUI with RTL support
- 🗨️ Chat-like interface with message history
- 🧠 Advanced AI powered by OpenAI
- 💻 Ability to control and manage the operating system
- 🔍 Smart product search and analysis
- 📊 System resource monitoring (CPU, RAM, Disk)
- 🎨 Beautiful and responsive user interface
- 🔤 Full Persian language support with optimized fonts

## 🚀 Installation & Setup

### Prerequisites

- Python 3.13 or higher
- Windows 10/11
- Valid OpenAI API key

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/TahaNili/Sofware-AI.git
cd Sofware-AI
```

2. Configure OpenAI key:
- Create a `.env` file in the project root
- Add your API key:
```env
OPENAI_API_KEY=your_api_key_here
```

3. Run the setup script:
- Open PowerShell as Administrator
- Navigate to the project directory
- Run the setup script:
```powershell
./setup_and_run.bat
```

## 💡 Usage

After running the application, you can:

1. **Product Search & Analysis**:
   - "What is the price of iPhone 13?"
   - "What is the best laptop under 20 million?"

2. **System Management**:
   - "Check CPU and RAM status"
   - "Open Photoshop application"

3. **Guidance & Advice**:
   - "Which camera do you recommend for photography?"
   - "What is the difference between MacBook Air and Pro?"

## 🧰 Technologies

- **Artificial Intelligence**: OpenAI GPT
- **User Interface**: PySide6 (Qt)
- **Programming Language**: Python 3.13
- **System Management**: PyWin32, PSUtil
- **Data Processing**: Pandas, NumPy

## 📝 Project Structure

```
Sofware-AI/
├── agent/                 # Core program logic
│   ├── windows/          # Windows management modules
│   ├── planner.py        # AI-powered planning
│   └── executor.py       # Command execution
├── ui/                   # User Interface
│   ├── main_window.py    # Modern Gemini-like GUI
│   ├── styles.py         # Modern UI styling
│   └── fonts/           # Persian fonts
└── main.py               # Entry point
```

## 📋 Development Guidelines

### Mandatory Rules

1. **Immediate Version Control**
   - Every change must be immediately committed with a detailed English commit message
   - Changes should be pushed to GitHub right after committing
   - Commit messages should clearly describe what changed and why

2. **Documentation First**
   - All new features must be documented in README.md
   - Update the Features section when adding new functionality
   - Keep documentation in sync with code changes

3. **Code Cohesion**
   - All code pieces must be logically related
   - Maintain clean architecture principles
   - Regular code reviews to ensure proper code organization
   - Report any unrelated or poorly organized code immediately

4. **Modularity**
   - Project must maintain a modular structure
   - Each module should have a single, well-defined responsibility
   - Minimize dependencies between modules
   - Follow the established project structure in the Project Structure section

## 🤝 Contributing

We welcome your contributions! Please:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a Pull Request
   - Ensure you follow all Development Guidelines above
   - Update README.md if adding new features

## 📄 License

This project is released under the MIT License. For details, see the [LICENSE](LICENSE) file.

## ⚠️ Troubleshooting

1. **PySide6 installation error**:
   ```bash
   pip install PySide6==6.10.0 --no-cache-dir
   ```

2. **OPENAI_API_KEY error**:
   - Make sure `.env` is properly configured
   - Check your API key

3. **Persian font issue**:
   - The application will automatically use Vazir font if available
   - If not available, it will fall back to system fonts with Persian support (Tahoma, Arial, Segoe UI)
   - For best results, install Vazir font from [Vazir-Font repository](https://github.com/rastikerdar/vazir-font)