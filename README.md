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

You can customize file categories by editing `config.json`:

```json
{
    "categories": {
        "Documents": [".pdf", ".docx", ".txt"],
        "Images": [".jpg", ".png"],
        "YourCustomCategory": [".ext1", ".ext2"]
    }
}
```

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
