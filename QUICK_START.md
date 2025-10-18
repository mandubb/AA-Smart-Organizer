# 🚀 Quick Start Guide - AA Smart Organizer

## Installation (First Time Only)

1. **Open Command Prompt or PowerShell** in this folder
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

**Simply run:**
```bash
python main.py
```

## How to Use

### Step 1: Select a Folder
- Click the **"📁 Browse"** button
- Choose a messy folder (e.g., Downloads, Desktop, Documents)
- The app will show how many files can be organized

### Step 2: Organize Files
- Click **"✨ Organize Files"**
- Watch the progress bar as files are sorted
- Review the summary in the activity log

### Step 3: Check Results
Your files are now organized into subfolders:
- 📄 **Documents** - PDFs, Word docs, Excel files, CSV, Markdown, etc.
- 🖼️ **Images** - JPG, PNG, GIF, SVG, HEIC, RAW, etc.
- 🎥 **Videos** - MP4, MKV, AVI, MOV, 3GP, MTS, etc.
- 🎵 **Music** - MP3, WAV, FLAC, MIDI, etc.
- ⚙️ **Installers** - EXE, MSI, APK, AppImage, etc.
- 📦 **Archives** - ZIP, RAR, 7Z, XZ, etc.
- 💻 **Code** - Python, JavaScript, HTML, CSS, PHP, TypeScript, etc.
- 🎮 **Game Files** - ROMs, save files, mods, etc.
- 🖥️ **System** - DLL, INI, CFG, LOG, etc.
- 🎨 **Design** - PSD, AI, Figma, Blender, etc.
- 💾 **Backups** - IMG, VHD, BAK, etc.
- 📚 **eBooks** - EPUB, MOBI, CBZ, etc.
- 🔌 **Plugins & Mods** - VST, ESP, BSA, etc.

**Total: 14 categories with 100+ file types!**

### Step 4: Undo (If Needed)
- Click **"↶ Undo Last Action"**
- All files return to their original locations
- Category folders are automatically removed if empty

## Tips

✅ **Safe to Use** - The app only moves files, never deletes them  
✅ **Undo Anytime** - Every organization can be undone  
✅ **No Duplicates** - Files with same names get numbered (file_1.pdf, file_2.pdf)  
✅ **Non-Blocking** - The UI stays responsive during organization  

## Customization

### Adding Your Own Categories

1. **Open** `config.json` in any text editor
2. **Edit** the file types - add/remove extensions or create new categories
3. **Save** the file
4. **Click** the **"🔄 Reload Config"** button in the app

Example - Adding a custom category:

```json
{
    "file_types": {
        "Documents": [".pdf", ".docx", ".txt"],
        "My Custom Category": [".ext1", ".ext2", ".ext3"]
    }
}
```

**See `CONFIG_GUIDE.md` for detailed customization instructions!**

## Troubleshooting

**Problem:** "No module named 'customtkinter'"  
**Solution:** Run `pip install customtkinter`

**Problem:** Files not organizing  
**Solution:** Check that files have extensions listed in `config.json`

**Problem:** Undo not working  
**Solution:** Don't manually move files after organizing - use the Undo button

## Creating a Standalone .exe

Want to share with others without Python?

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AA Smart Organizer" main.py
```

The `.exe` file will be in the `dist/` folder.

---

**Made with ❤️ by AA's Computer and Remote Services**
