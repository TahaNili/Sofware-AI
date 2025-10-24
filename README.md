# 🤖 Sofware-AI

An intelligent assistant for Windows OS with a graphical user interface and full support for Persian language.

## ✨ Features

- 🎯 Modern and clean GUI with RTL support
- 🗨️ Professional chat interface with message history
- 🧠 Advanced AI powered by OpenAI and Google Gemini
- 💻 Complete Windows OS Control:
  - 🖥️ System resource monitoring (CPU, RAM, Disk usage)
  - 📦 Automated software installation and management
  - 🚀 Process and application control
  - 🔍 File system navigation and management
- 🌐 Advanced Web Integration:
  - � Real-time product search and price comparison
  - 📊 Market analysis and recommendations
  - � Online shopping assistance
  - 📱 Product reviews and specifications
- 🤖 System Automation:
  - ⚡ Task scheduling and automation
  - 📥 Automated software downloads
  - 🔄 System maintenance tasks
  - 🎛️ Settings management
- 🎨 Beautiful and responsive user interface
- 🔤 Full Persian language support with optimized fonts

## 🚀 Installation & Setup

### Prerequisites

- Python 3.13 or higher
- Windows 10/11
- Either:
  - Valid Google API key for Gemini (Recommended, Free)
  - Valid OpenAI API key (Optional)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/TahaNili/Sofware-AI.git
cd Sofware-AI
```

2. Configure AI Provider:
- Create a `.env` file in the project root
- Add your API key(s):
```env
# For Google Gemini (Recommended, Free)
GOOGLE_API_KEY=your_google_api_key_here

# For OpenAI (Optional)
OPENAI_API_KEY=your_openai_api_key_here
```
Note: You only need to set one of the API keys. The application will automatically use Gemini if `GOOGLE_API_KEY` is set.

3. Run the setup script:
- Open PowerShell as Administrator
- Navigate to the project directory
- Run the setup script:
```powershell
./setup_and_run.bat
```

## 💡 Usage

After running the application, you can:

1. **System Control & Monitoring**:
   - "بررسی وضعیت CPU و RAM سیستم"
   - "اجرای فتوشاپ"
   - "نمایش برنامه‌های در حال اجرا"
   - "پاکسازی فایل‌های موقت"
   - "بررسی دمای CPU"

2. **Software Management**:
   - "دانلود و نصب Chrome"
   - "به‌روزرسانی درایورها"
   - "حذف برنامه X"
   - "نصب آخرین نسخه Visual Studio Code"

3. **Web & Shopping Assistant**:
   - "بهترین لپ‌تاپ زیر 20 میلیون"
   - "مقایسه قیمت گوشی سامسونگ S23"
   - "بررسی نظرات کاربران درباره ایرپاد پرو"
   - "پیدا کردن ارزان‌ترین قیمت PS5"

4. **System Automation**:
   - "زمانبندی خاموش شدن سیستم"
   - "بکاپ‌گیری خودکار از پوشه Projects"
   - "اجرای خودکار برنامه‌ها در استارت‌آپ"
   - "بهینه‌سازی عملکرد سیستم"

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

## Browser-Use integration and dependency conflict

Note: The `browser-use` library requires older OpenAI 1.x API (openai < 2.0.0). Many newer packages — and some parts of this project — may require OpenAI 2.x.

To avoid breaking the main environment we provide an isolated environment option for browser-use. This keeps the `openai` package required by `browser-use` pinned to a compatible 1.x version while the main project can continue using OpenAI 2.x if necessary.

Recommended setup (PowerShell):

```powershell
# Create an isolated virtualenv for browser-use
python -m venv .venv-browser
# Activate it
.\\.venv-browser\\Scripts\\Activate.ps1
# Install the browser-specific requirements (this pins openai to <2.0.0)
pip install -r requirements-browser.txt
# Install any browser drivers (Playwright) if needed:
# playwright install
```

Using the wrapper in the repository:

- The project includes `agent/ai/browser_use_wrapper.py` which runs commands inside `.venv-browser`.

Example: run a browser-use command from the project root (PowerShell):

```powershell
# from repo root
python .\\agent\\ai\\browser_use_wrapper.py -m browser_use some_command
```

Integration approaches (choose one):

1. Run `browser_use_wrapper` subprocess from the main application whenever you need the browser-use features. This keeps the environments isolated and avoids dependency conflicts.
2. If you prefer a single environment, pin `openai` in `requirements.txt` to `>=1.99.2,<2.0.0` and rework code that depends on OpenAI 2.x features.

If you want, I can:
- Create a small CLI script that talks to the wrapper via stdin/stdout or a local socket.
- Or pin `openai` to `<2.0.0` and update the codebase to be compatible with OpenAI 1.x.

Which approach would you like me to implement? (I recommend the isolated virtualenv + wrapper approach.)