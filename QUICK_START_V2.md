# 🚀 Quick Start Guide - AA Smart Organizer v2.0

Get started with the new modular features in under 5 minutes!

---

## 📦 Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify installation
python test_modular_system.py
```

---

## 🎯 Quick Examples

### Example 1: Basic Organization (CLI)

```bash
# Organize your Downloads folder
python main_cli.py organize "C:\Users\YourName\Downloads"
```

**What happens:**
- Files are sorted into categories (Documents, Images, Videos, etc.)
- Activity log is created in `profiles/default/logs/`
- Summary report is generated
- Undo data is saved

---

### Example 2: Organization with Cleanup

```bash
# Clean junk files first, then organize
python main_cli.py organize "C:\Users\YourName\Downloads" --quick-clean
```

**What happens:**
- Removes `.tmp`, `.log`, `Thumbs.db`, etc.
- Deletes empty folders
- Then organizes remaining files
- Shows space freed

---

### Example 3: Preview Cleanup (Safe)

```bash
# See what will be cleaned WITHOUT deleting
python main_cli.py quick-clean "C:\Users\YourName\Downloads" --preview
```

**What happens:**
- Scans for junk files
- Shows what would be deleted
- Shows how much space would be freed
- **Does NOT delete anything**

---

### Example 4: Multiple Client Profiles

```bash
# Create profiles for different clients
python main_cli.py create-profile client_a
python main_cli.py create-profile client_b

# Work with Client A
python main_cli.py switch-profile client_a
python main_cli.py organize "C:\ClientA\Files"

# Work with Client B
python main_cli.py switch-profile client_b
python main_cli.py organize "C:\ClientB\Files"

# Each client has separate:
# - Configuration
# - Activity logs
# - File categories
```

---

### Example 5: GUI Mode (Original)

```bash
# Launch the graphical interface
python main.py
```

**Features:**
- Browse and select folders
- Visual progress bar
- Activity log display
- Undo button
- Reload config button

---

## 📊 Understanding the Output

### CLI Organization Output

```
======================================================================
🗂️  AA SMART ORGANIZER - DEFAULT PROFILE
======================================================================
Target Folder: C:\Downloads
Started: 2024-10-18 14:30:00
======================================================================

📊 Found 150 files, 120 can be organized

🚀 Organizing files...

  Progress: 150/150 files processed...

======================================================================
📊 OPERATION SUMMARY
======================================================================
Timestamp: 2024-10-18 14:30:15
Duration: 15.23 seconds
----------------------------------------------------------------------

📈 STATISTICS:
  Total Files Processed: 150
  Files Organized: 120
  Files Skipped: 25
  Files Failed: 5
  Success Rate: 80.0%
  Total Size Moved: 2.5 GB

📁 BY CATEGORY:
  Documents.....................   50 files ( 41.7%) ████████
  Images........................   40 files ( 33.3%) ██████
  Videos........................   20 files ( 16.7%) ███
  Music.........................   10 files (  8.3%) █

🏆 Most Active Category: Documents (50 files)

======================================================================

📄 Summary saved to: logs/summary_20241018_143015.txt
```

---

## 🗂️ Where Are My Files?

### After Organization

```
Your Folder/
├── Documents/          # .pdf, .docx, .txt, etc.
│   ├── report.pdf
│   └── notes.txt
├── Images/             # .jpg, .png, .gif, etc.
│   ├── photo1.jpg
│   └── screenshot.png
├── Videos/             # .mp4, .mkv, .avi, etc.
│   └── movie.mp4
├── Music/              # .mp3, .wav, .flac, etc.
│   └── song.mp3
└── unorganized.xyz     # Files without categories stay here
```

---

## 📝 Where Are My Logs?

### Log Locations

```
AA Smart Organizer/
├── logs/                           # Global logs
│   ├── activity_2024-10-18.txt   # Daily activity log
│   ├── activity_2024-10-18.csv   # CSV export
│   └── summary_*.txt              # Summary reports
│
└── profiles/
    ├── default/
    │   └── logs/                   # Default profile logs
    │       ├── activity_*.txt
    │       ├── activity_*.csv
    │       └── undo_data.json      # For undo functionality
    │
    └── client_a/
        └── logs/                   # Client A profile logs
            └── ...
```

---

## 🔄 How to Undo

### Method 1: GUI
1. Open `python main.py`
2. Click "↶ Undo Last Action"
3. Files are restored to original locations

### Method 2: Manual
1. Check `profiles/[profile]/logs/undo_data.json`
2. See original file locations
3. Move files back manually if needed

---

## ⚙️ Customizing Categories

### Add Your Own Categories

1. Open `config.json` (or `profiles/[profile]/config.json`)
2. Add your category:

```json
{
    "file_types": {
        "Documents": [".pdf", ".docx"],
        "Images": [".jpg", ".png"],
        
        "My Custom Category": [".custom", ".xyz"],
        "Blender Projects": [".blend", ".blend1"],
        "CAD Files": [".dwg", ".dxf", ".step"]
    }
}
```

3. Reload config:
   - **GUI**: Click "🔄 Reload Config"
   - **CLI**: Just run again (auto-loads)

4. Organize files - new folders are created automatically!

---

## 🧹 Quick Clean Details

### What Gets Cleaned

**Junk Files:**
- `.tmp`, `.temp` - Temporary files
- `.log` - Log files
- `.cache` - Cache files
- `.bak`, `.old` - Backup files
- `Thumbs.db` - Windows thumbnails
- `desktop.ini` - Windows system files
- `.DS_Store` - macOS system files
- `~$*` - Office temporary files

**Empty Folders:**
- Any folder with no files or subfolders

**Optional:**
- Windows Recycle Bin (if enabled in config)

---

## 🎨 Viewing HTML Reports

After organizing, you can generate beautiful HTML reports:

```python
# In Python
from modules import SummaryGenerator

summary = SummaryGenerator()
# ... after organizing ...
summary.export_to_html("report.html")
```

Then open `report.html` in your browser for a professional report with:
- Color-coded statistics
- Bar charts
- Category breakdowns
- Professional styling

---

## 🕒 Scheduling (Advanced)

### Schedule Daily Organization

```python
from modules import TaskScheduler
from pathlib import Path

scheduler = TaskScheduler(Path("scheduler_config.json"))

# Add daily schedule
scheduler.add_schedule(
    schedule_type="daily",
    time_str="14:30",  # 2:30 PM
    folder_path="C:/Downloads",
    profile="default",
    quick_clean=True
)

# Start scheduler (runs in background)
scheduler.start(task_callback=your_organize_function)
```

---

## 🆘 Troubleshooting

### "No module named 'schedule'"
```bash
pip install schedule
```

### "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Files Not Being Organized
1. Check if file extension is in `config.json`
2. Look at activity log for errors
3. Verify folder path is correct

### Profile Not Found
```bash
# List available profiles
python main_cli.py list-profiles

# Create if missing
python main_cli.py create-profile [name]
```

### Logs Taking Up Space
- Logs auto-rotate after 30 days (configurable)
- Set `log_rotation_days` in `config.json`
- Or manually delete old logs from `logs/` folder

---

## 📚 Next Steps

1. **Read Full Documentation**: [README_MODULAR.md](README_MODULAR.md)
2. **Customize Categories**: [CUSTOM_CATEGORIES_GUIDE.md](CUSTOM_CATEGORIES_GUIDE.md)
3. **Explore Modules**: Check `modules/` folder for advanced features
4. **Create Profiles**: Set up profiles for different use cases
5. **Automate**: Set up scheduling for regular maintenance

---

## 💡 Pro Tips

1. **Always Preview First**: Use `--preview` with quick-clean before deleting
2. **Use Profiles**: Keep work and personal files separate
3. **Check Logs**: Review activity logs for audit trails
4. **Export Summaries**: Save HTML reports for documentation
5. **Customize Categories**: Add categories for your specific workflow
6. **Schedule Maintenance**: Set up weekly quick-clean tasks
7. **Backup Configs**: Export profiles before major changes

---

## 🎯 Common Workflows

### Workflow 1: Daily Downloads Cleanup
```bash
# Every day at 5 PM
python main_cli.py organize "C:\Downloads" --quick-clean
```

### Workflow 2: Client Project Organization
```bash
# Create client profile
python main_cli.py create-profile client_xyz

# Switch to client profile
python main_cli.py switch-profile client_xyz

# Organize client files
python main_cli.py organize "C:\Projects\ClientXYZ"
```

### Workflow 3: Weekly Maintenance
```bash
# Monday morning cleanup
python main_cli.py quick-clean "C:\Downloads"
python main_cli.py quick-clean "C:\Desktop"
python main_cli.py quick-clean "C:\Documents"
```

---

## 🤝 Getting Help

- **Documentation**: See `README_MODULAR.md`
- **Examples**: Run `test_modular_system.py`
- **Support**: Contact AA's Computer and Remote Services

---

**Made with ❤️ by AA's Computer and Remote Services**

*Professional File Organization & Maintenance System v2.0*
