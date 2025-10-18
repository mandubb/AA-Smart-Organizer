# 🗂️ AA Smart Organizer

**A modern Python desktop application that automatically organizes messy folders into neatly categorized subfolders.**

---

## ✨ Features

- **📁 Folder Selection** - Easy browse button to select any folder
- **🎯 Smart Categorization** - Automatically sorts files by type:
  - 📄 **Documents** → `.pdf`, `.docx`, `.txt`, `.xlsx`, etc.
  - 🖼️ **Images** → `.jpg`, `.png`, `.gif`, `.svg`, etc.
  - 🎥 **Videos** → `.mp4`, `.mkv`, `.avi`, `.mov`, etc.
  - 🎵 **Music** → `.mp3`, `.wav`, `.flac`, `.aac`, etc.
  - ⚙️ **Installers** → `.exe`, `.msi`, `.dmg`, `.apk`, etc.
  - 📦 **Archives** → `.zip`, `.rar`, `.7z`, `.tar`, etc.
  - 💻 **Code** → `.py`, `.js`, `.html`, `.css`, `.java`, etc.

- **🎨 Fully Customizable** - Add your own categories without touching code!
  - Edit `config.json` to add custom categories (e.g., "Blender Projects", "CAD Files")
  - Folders are created automatically during organization
  - Invalid entries are skipped gracefully with warnings
  - See [CUSTOM_CATEGORIES_GUIDE.md](CUSTOM_CATEGORIES_GUIDE.md) for detailed instructions

- **📊 Progress Tracking** - Real-time progress bar and file counter
- **↶ Undo Functionality** - Restore files to original locations with one click
- **📝 Activity Log** - Detailed summary of all operations
- **🎨 Modern UI** - Clean, dark-themed interface built with CustomTkinter

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download this repository**
   ```bash
   cd "AA Smart Organizer"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

---

## 📖 How to Use

1. **Launch the app** by running `python main.py`
2. **Click "📁 Browse"** to select a folder you want to organize
3. **Review the file count** - the app shows how many files can be organized
4. **Click "✨ Organize Files"** to start the organization process
5. **Watch the progress** - see real-time updates as files are sorted
6. **Review the summary** - check the activity log for detailed results
7. **Use "↶ Undo Last Action"** if you want to restore files to their original locations

---

## 🗂️ Project Structure

```
AA Smart Organizer/
├── main.py              # Main application with GUI
├── organizer.py         # File organization logic
├── undo_manager.py      # Undo functionality
├── config.json          # File type categories configuration
├── undo_log.json        # Auto-generated undo history
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## ⚙️ Configuration

### Customizing File Categories

**AA Smart Organizer is fully user-customizable!** You can add, edit, or remove file categories directly in `config.json` without modifying any Python code.

#### Quick Start

1. **Open** `config.json` in any text editor
2. **Add your custom category:**
   ```json
   {
       "file_types": {
           "Documents": [".pdf", ".docx", ".txt"],
           "Images": [".jpg", ".png"],
           "Blender Projects": [".blend", ".blend1"],
           "CAD Files": [".dwg", ".dxf", ".step"]
       }
   }
   ```
3. **Save** the file
4. **Click** the "🔄 Reload Config" button in the app
5. **Organize!** Folders are created automatically

#### 📚 Comprehensive Guide

For detailed instructions, examples, and troubleshooting, see:
**[CUSTOM_CATEGORIES_GUIDE.md](CUSTOM_CATEGORIES_GUIDE.md)**

This guide includes:
- ✅ Valid and invalid configuration examples
- ✅ Real-world use cases (developers, designers, students)
- ✅ Validation rules and error handling
- ✅ Tips and best practices

#### Key Features

- **🎯 Fully Dynamic** - Read all categories from `config.json` at runtime
- **📁 Auto-Folder Creation** - Folders are created automatically during organization
- **✅ Graceful Validation** - Invalid entries are skipped with warnings (won't break the app)
- **🔄 Hot Reload** - Apply changes without restarting the app
- **🛡️ Safe Defaults** - Missing config is auto-created with 17 default categories
- **💾 Preservation** - User categories are preserved even if config regenerates

---

## 🔮 Future Enhancements

- [ ] Include subfolders option
- [ ] Send junk files to Recycle Bin
- [ ] Scheduled auto-organize (weekly cleanup)
- [ ] Light/Dark theme switcher
- [ ] Desktop notifications
- [ ] Portable .exe build with PyInstaller

---

## 🛠️ Tech Stack

- **Python 3** - Core language
- **CustomTkinter** - Modern GUI framework
- **pathlib** - Cross-platform path handling
- **shutil** - File operations
- **json** - Configuration and undo log storage
- **threading** - Non-blocking UI operations

---

## 📝 License

This project is created for **AA's Computer and Remote Services**.

---

## 👨‍💻 Developer Notes

### Building an Executable

To create a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AA Smart Organizer" main.py
```

The executable will be in the `dist/` folder.

---

## 🐛 Troubleshooting

**Issue: "No module named 'customtkinter'"**
- Solution: Run `pip install customtkinter`

**Issue: Files not organizing**
- Check that the folder path is correct
- Ensure files have recognized extensions (check `config.json`)
- Review the activity log for error messages

**Issue: Undo not working**
- Ensure `undo_log.json` exists and is not corrupted
- Check that files haven't been manually moved after organization

---

## 📧 Support

For support or feature requests, contact **AA's Computer and Remote Services**.

---

**Made with ❤️ by AA's Computer and Remote Services**
