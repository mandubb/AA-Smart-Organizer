# 🗂️ AA Smart Organizer v2.0 - Modular Professional Edition

**A comprehensive, modular file organization and maintenance system with advanced features for professional use.**

---

## 🚀 What's New in v2.0

### **Complete Modular Architecture**
- Separated concerns into independent, reusable modules
- Profile-based configuration system
- Advanced activity logging with undo support
- Smart maintenance and cleanup tools
- Automated scheduling capabilities
- Professional summary reports

---

## 📁 Project Structure

```
AA Smart Organizer/
├── main.py                      # GUI Application (existing)
├── main_cli.py                  # NEW: CLI Interface
├── organizer.py                 # Core organization logic
├── undo_manager.py              # Undo functionality
├── config.json                  # Global configuration
├── requirements.txt             # Python dependencies
│
├── modules/                     # NEW: Modular components
│   ├── __init__.py             # Module exports
│   ├── utils.py                # Utility functions
│   ├── activity_log.py         # Activity logging system
│   ├── maintenance.py          # Cleanup and maintenance
│   ├── profiles.py             # Profile management
│   ├── summary.py              # Summary generation
│   └── scheduler.py            # Task scheduling
│
├── profiles/                    # NEW: User profiles
│   └── default/
│       ├── config.json         # Profile-specific config
│       └── logs/               # Profile-specific logs
│
└── logs/                        # NEW: Global logs
    └── activity_*.txt          # Daily activity logs
```

---

## ✨ Core Features

### 1. 🧠 Smart Activity Log
**Module:** `modules/activity_log.py`

- **Detailed Logging**: Every file operation is logged with:
  - Timestamp
  - Filename
  - Old path → New path
  - File size
  - Category
  - Status (Success/Failed)

- **Multiple Formats**:
  - Plain text logs (`activity_YYYY-MM-DD.txt`)
  - CSV exports (`activity_YYYY-MM-DD.csv`)
  - JSON undo data

- **Undo Support**: Restore files to original locations

- **Automatic Rotation**: Old logs are automatically deleted after configurable days

**Example:**
```python
from modules import ActivityLog

log = ActivityLog(Path("logs"))
log.log_move("document.pdf", old_path, new_path, 1024000, "Documents", "Success")
log.save_undo_data()
```

---

### 2. 🧹 Auto Maintenance Mode - "Quick Clean"
**Module:** `modules/maintenance.py`

Automatically detects and removes:
- Temporary files (`.tmp`, `.temp`, `.cache`)
- System junk (`Thumbs.db`, `desktop.ini`, `.DS_Store`)
- Office temp files (`~$*`)
- Log files (`.log`)
- Empty folders

**Features:**
- Preview mode (scan without deleting)
- Recursive scanning
- Space calculation
- Windows Recycle Bin clearing
- Detailed cleanup reports

**Example:**
```python
from modules import MaintenanceManager

maintenance = MaintenanceManager()
stats = maintenance.quick_clean(
    directory=Path("C:/Downloads"),
    recursive=False,
    preview_only=False,
    clear_recycle_bin=True
)
print(f"Freed: {stats['space_freed_formatted']}")
```

---

### 3. 👤 User Profiles
**Module:** `modules/profiles.py`

Each profile has:
- Separate configuration (`config.json`)
- Independent log directory
- Custom file categories
- Metadata (created, last used)

**Operations:**
- Create new profiles
- Switch between profiles
- Import/Export profiles
- Delete profiles (except default)

**Example:**
```python
from modules import ProfileManager

profiles = ProfileManager(Path("profiles"))
profiles.create_profile("client1")
profiles.load_profile("client1")
config = profiles.load_config()
```

---

### 4. 📊 Smart Summary Dashboard
**Module:** `modules/summary.py`

Generates comprehensive reports with:
- Total files processed
- Files organized/skipped/failed
- Success rate percentage
- Total size moved
- Category breakdown with percentages
- Most active category
- Operation duration

**Export Formats:**
- CLI display (colored, formatted)
- Plain text reports
- HTML reports (with charts and styling)

**Example:**
```python
from modules import SummaryGenerator

summary = SummaryGenerator()
summary.start_operation()
# ... perform operations ...
summary.end_operation()

data = summary.generate_summary(
    total_files=100,
    files_organized=95,
    files_skipped=3,
    files_failed=2,
    total_size=524288000,
    categories={"Documents": 50, "Images": 45}
)

summary.print_cli_summary()
summary.export_to_html(Path("report.html"))
```

---

### 5. ⚡ Quick Clean Mode
**Integrated Feature**

Lightweight cleanup without full organization:
- Fast junk file detection
- Preview before deletion
- User confirmation
- Minimal system impact

**CLI Usage:**
```bash
python main_cli.py quick-clean "C:\Downloads" --preview
python main_cli.py quick-clean "C:\Downloads"
```

---

### 6. 🕒 Auto-Scheduler
**Module:** `modules/scheduler.py`

Schedule automatic organization tasks:
- **Daily**: Run at specific time every day
- **Weekly**: Run on specific day and time
- **Monthly**: Run on first day of month

**Features:**
- Multiple schedules per profile
- Email notifications (SMTP)
- Windows Task Scheduler integration
- Next run time tracking
- Enable/disable individual schedules

**Example:**
```python
from modules import TaskScheduler

scheduler = TaskScheduler(Path("scheduler_config.json"))
scheduler.add_schedule(
    schedule_type="daily",
    time_str="14:30",
    folder_path="C:/Downloads",
    profile="default",
    quick_clean=True
)
scheduler.start(task_callback=organize_function)
```

---

## ⚙️ Configuration

### Global Config (`config.json`)

```json
{
    "enable_activity_log": true,
    "enable_quick_clean": true,
    "enable_profiles": true,
    "enable_summary": true,
    "enable_scheduler": false,
    "log_rotation_days": 30,
    
    "file_types": {
        "Documents": [".pdf", ".docx", ".txt"],
        "Images": [".jpg", ".png", ".gif"],
        "Videos": [".mp4", ".mkv", ".avi"],
        "Music": [".mp3", ".wav", ".flac"],
        "Code": [".py", ".js", ".html", ".css"]
    },
    
    "maintenance": {
        "auto_clean_junk": false,
        "remove_empty_folders": true,
        "clear_recycle_bin": false
    },
    
    "scheduler": {
        "enabled": false,
        "schedules": []
    }
}
```

### Profile Config (`profiles/[name]/config.json`)

Each profile can override global settings and define custom categories.

---

## 🖥️ CLI Usage

### Basic Organization
```bash
# Organize a folder
python main_cli.py organize "C:\Downloads"

# Organize with quick clean first
python main_cli.py organize "C:\Downloads" --quick-clean
```

### Quick Clean
```bash
# Preview what will be cleaned
python main_cli.py quick-clean "C:\Downloads" --preview

# Actually clean
python main_cli.py quick-clean "C:\Downloads"
```

### Profile Management
```bash
# List all profiles
python main_cli.py list-profiles

# Create new profile
python main_cli.py create-profile work

# Switch to profile
python main_cli.py switch-profile work
```

---

## 🎨 GUI Usage

The existing GUI (`main.py`) continues to work with all original features:
- Browse and select folders
- Organize files with progress tracking
- Undo last operation
- Reload configuration
- Activity log display

**To launch GUI:**
```bash
python main.py
```

---

## 📋 Module Reference

### Utils Module (`modules/utils.py`)
Common utility functions used across all modules:
- `format_file_size(bytes)` - Human-readable file sizes
- `get_file_size(path)` - Get file size safely
- `ensure_directory(path)` - Create directory if needed
- `load_json(path)` - Load JSON with error handling
- `save_json(path, data)` - Save JSON safely
- `get_timestamp()` - Current timestamp string
- `is_junk_file(filename)` - Check if file is junk
- `calculate_duration(start, end)` - Format duration

### Activity Log Module
- `ActivityLog(log_directory)` - Initialize logger
- `log_move(...)` - Log file move operation
- `log_delete(...)` - Log file deletion
- `log_action(...)` - Log general action
- `save_undo_data()` - Save for undo
- `load_undo_data()` - Load undo data
- `get_session_summary()` - Get statistics
- `rotate_logs(days)` - Delete old logs
- `export_session_to_file(path)` - Export report

### Maintenance Module
- `MaintenanceManager(log_callback)` - Initialize manager
- `is_junk_file(path)` - Check if file is junk
- `scan_junk_files(dir, recursive)` - Find junk files
- `find_empty_folders(dir)` - Find empty folders
- `delete_junk_files(files)` - Delete junk files
- `delete_empty_folders(folders)` - Delete empty folders
- `clear_recycle_bin_windows()` - Clear Recycle Bin
- `quick_clean(dir, ...)` - Full cleanup operation
- `get_cleanup_report()` - Get detailed report

### Profiles Module
- `ProfileManager(profiles_dir)` - Initialize manager
- `create_profile(name)` - Create new profile
- `list_profiles()` - List all profiles
- `load_profile(name)` - Load profile
- `get_current_profile()` - Get active profile
- `load_config()` - Load profile config
- `save_config(data)` - Save profile config
- `delete_profile(name)` - Delete profile
- `export_profile(name, path)` - Export to ZIP
- `import_profile(path, name)` - Import from ZIP

### Summary Module
- `SummaryGenerator()` - Initialize generator
- `start_operation()` - Mark start time
- `end_operation()` - Mark end time
- `generate_summary(...)` - Create summary data
- `print_cli_summary()` - Display in CLI
- `export_to_text(path)` - Export as text
- `export_to_html(path)` - Export as HTML
- `generate_quick_summary(...)` - One-line summary

### Scheduler Module
- `TaskScheduler(config_path)` - Initialize scheduler
- `add_schedule(...)` - Add new schedule
- `remove_schedule(id)` - Remove schedule
- `list_schedules()` - List all schedules
- `setup_schedules(callback)` - Setup with schedule library
- `start(callback)` - Start scheduler loop
- `stop()` - Stop scheduler
- `send_email_report(...)` - Send email
- `configure_email(...)` - Setup email
- `create_windows_task(...)` - Create Windows Task

---

## 🔧 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Profiles
Profiles are created automatically on first run.

### 3. Run Application
```bash
# GUI
python main.py

# CLI
python main_cli.py --help
```

---

## 📊 Example Workflow

### Scenario: Organize Downloads with Cleanup

```bash
# 1. Preview what will be cleaned
python main_cli.py quick-clean "C:\Downloads" --preview

# 2. Organize with automatic cleanup
python main_cli.py organize "C:\Downloads" --quick-clean

# 3. Check the summary
# (Automatically displayed and saved to logs/)

# 4. View activity log
type logs\activity_2024-10-18.txt
```

### Scenario: Multiple Client Profiles

```bash
# Create profiles for different clients
python main_cli.py create-profile client_a
python main_cli.py create-profile client_b

# Organize for Client A
python main_cli.py switch-profile client_a
python main_cli.py organize "C:\ClientA\Files"

# Organize for Client B
python main_cli.py switch-profile client_b
python main_cli.py organize "C:\ClientB\Files"

# Each client has separate logs and configs
```

---

## 🎯 Best Practices

1. **Use Profiles**: Create separate profiles for different use cases
2. **Preview First**: Use `--preview` with quick-clean before deleting
3. **Regular Cleanup**: Run quick-clean periodically
4. **Check Logs**: Review activity logs for audit trails
5. **Export Summaries**: Save HTML reports for documentation
6. **Rotate Logs**: Configure `log_rotation_days` appropriately
7. **Test Schedules**: Test scheduled tasks manually first

---

## 🛡️ Safety Features

- **Undo Support**: All move operations can be undone
- **Preview Mode**: See what will be deleted before committing
- **Validation**: Invalid configurations are handled gracefully
- **Error Logging**: All errors are logged for debugging
- **Backup Profiles**: Export profiles before major changes
- **No Data Loss**: Files that don't match categories stay in place

---

## 🚀 Future Enhancements

- [ ] Web-based dashboard
- [ ] Real-time monitoring
- [ ] Cloud storage integration
- [ ] Advanced file deduplication
- [ ] Machine learning categorization
- [ ] Multi-language support
- [ ] Plugin system

---

## 📚 Documentation

- **User Guide**: See `CUSTOM_CATEGORIES_GUIDE.md` for category customization
- **API Reference**: Module docstrings provide detailed API documentation
- **Examples**: Check `test_custom_categories.py` for usage examples
- **Changelog**: See `CHANGELOG_CUSTOM_CATEGORIES.md` for version history

---

## 🤝 Support

For support, feature requests, or bug reports, contact:
**AA's Computer and Remote Services**

---

## 📄 License

Created for AA's Computer and Remote Services

---

**Made with ❤️ by AA's Computer and Remote Services**

*Professional File Organization & Maintenance System v2.0*
