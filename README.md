# ⚡ AA Smart Organizer

**A professional file organization and maintenance system with futuristic dark-themed GUI.**

> ✨ **Latest Features**: PDF Export, Safety Confirmation Dialogs, Recycle Bin Clearing, Enhanced UI  
> 🚀 **Automate Smarter** - Organize files, clean junk, and generate professional reports!

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

### ✨ Professional Features

- **🧠 Smart Activity Logging** - Detailed logs with timestamps and file tracking
- **🧹 Quick Clean Mode** - Remove junk files, empty folders, and clear Recycle Bin
- **⚠️ Safety Confirmation** - Warning dialog before any destructive operations
- **📊 PDF Export** - Generate professional PDF reports with tables and charts
- **👁️ Preview Mode** - See what will be deleted without actually deleting
- **✨🧹 Organize + Clean** - Two-in-one operation for maximum efficiency
- **🎨 Futuristic Theme** - Dark interface with cyan/blue/purple accents
- **🔧 Modular Architecture** - Clean, maintainable, extensible codebase

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
   
   Required packages:
   - `customtkinter` - Modern GUI framework
   - `reportlab` - PDF generation
   - `pillow` - Image support for PDFs
   - `schedule` - Task scheduling

3. **Run the application**
   ```bash
   python main_v2.py
   ```

---

## 📖 How to Use

### GUI Mode

1. **Launch the app** by running `python main_v2.py`
2. **Click "📁 Browse"** to select a folder you want to organize
3. **Review the file count** - the app shows how many files can be organized
4. **Choose an action:**
   - **✨ Organize Files** - Sort files into categories
   - **✨🧹 Organize + Clean** - Clean junk first, then organize
   - **🧹 Quick Clean** - Remove junk files and clear Recycle Bin (with confirmation)
   - **👁️ Preview Clean** - See what would be deleted (safe, no confirmation)
   - **📊 Export Summary** - Generate PDF/HTML/Text report
5. **Watch the progress** - see real-time updates in the activity log
6. **Use "↶ Undo Last Action"** if you want to restore organized files

### Quick Clean Features

**What Gets Deleted:**
- Temporary files: `.tmp`, `.temp`, `.log`, `.cache`
- System junk: `Thumbs.db`, `desktop.ini`, `.DS_Store`
- Office temp files: `~$*.docx`, `~$*.xlsx`
- Empty folders
- **Recycle Bin contents** (Windows)

**Safety Features:**
- ⚠️ **Confirmation Dialog** - Shows before any deletion
- Clear warning about permanent deletion
- Lists all file types that will be affected
- "Cancel" option to abort
- **Preview Mode** - See what would be deleted without deleting

---

## 🗂️ Project Structure

```
AA Smart Organizer/
├── main_v2.py                   # Main GUI Application
├── organizer.py                 # Core organization logic
├── undo_manager.py              # Undo functionality
├── config.json                  # Global configuration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── modules/                     # Modular components
│   ├── __init__.py
│   ├── utils.py                # Utility functions
│   ├── activity_log.py         # Activity logging
│   ├── maintenance.py          # Cleanup & maintenance
│   ├── summary.py              # Summary & PDF export
│   ├── scheduler.py            # Task scheduling
│   └── gui_futuristic.py       # Confirmation dialogs & theme
│
├── logs/                        # Activity logs
│   └── activity_log.txt
│
└── exports/                     # Exported reports
    └── summaries/
        └── *.pdf               # PDF reports
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

#### Example Categories

The default `config.json` includes 23+ categories:
- Documents, Images, Videos, Music
- Code, Design, Installers, Archives
- Game Files, eBooks, Torrents
- Backups, Plugins & Mods, System files
- And more!

**Add your own:**
```json
"3D Models": [".obj", ".fbx", ".blend", ".3ds"],
"Spreadsheets": [".xlsx", ".xls", ".csv", ".ods"]
```

#### Key Features

- **🎯 Fully Dynamic** - Read all categories from `config.json` at runtime
- **📁 Auto-Folder Creation** - Folders are created automatically during organization
- **✅ Graceful Validation** - Invalid entries are skipped with warnings (won't break the app)
- **🔄 Hot Reload** - Apply changes without restarting the app
- **🛡️ Safe Defaults** - Missing config is auto-created with 17 default categories
- **💾 Preservation** - User categories are preserved even if config regenerates

---

## 📊 PDF Export Features

**Professional Reports Include:**
- 📈 Statistics table (files processed, success rate, size moved)
- 📁 Category breakdown with percentages
- 🏆 Most active category
- ⏱️ Operation duration and timestamp
- 🎨 Color-coded tables and charts
- 📄 Custom footer: "Generated by AA Smart Organizer — Automate Smarter."

**Export Formats:**
- **PDF** - Professional reports (default)
- **HTML** - Web-viewable with charts
- **Text** - Simple plain text

**Usage:**
1. Organize some files
2. Click "📊 Export Summary"
3. Choose format (PDF recommended)
4. Save to `exports/summaries/`

---

## 🛠️ Tech Stack

- **Python 3.7+** - Core language
- **CustomTkinter** - Modern dark-themed GUI framework
- **ReportLab** - Professional PDF generation
- **Pillow** - Image processing for PDFs
- **pathlib** - Cross-platform path handling
- **shutil** - File operations
- **json** - Configuration storage
- **threading** - Non-blocking UI operations
- **ctypes** - Windows API for Recycle Bin clearing

---

## 📝 License

This project is created for **AA's Computer and Remote Services**.

---

## 👨‍💻 Developer Notes

### Building an Executable

To create a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AA Smart Organizer" main_v2.py
```

The executable will be in the `dist/` folder.

### Color Theme

**Futuristic Dark Theme:**
- Background: Deep space black (#0A0E27)
- Accents: Cyan (#00D9FF), Blue (#0066FF), Purple (#9D00FF)
- Success: Matrix green (#00FF88)
- Warning: Orange (#F59E0B)
- Text: White with blue-gray secondary

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

**Issue: Recycle Bin not clearing**
- Ensure you're running on Windows (feature is Windows-only)
- Check that you confirmed the warning dialog
- Preview mode does NOT clear Recycle Bin (by design)
- Look for "✅ Recycle Bin cleared" in the activity log

**Issue: PDF export fails**
- Ensure `reportlab` is installed: `pip install reportlab`
- Check that `exports/summaries/` directory exists
- Organize files first before exporting (need data to export)

---

## 📧 Support

For support or feature requests, contact **AA's Computer and Remote Services**.

---

**Made with ❤️ by AA's Computer and Remote Services**
