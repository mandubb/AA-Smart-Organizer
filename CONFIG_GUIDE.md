# 📝 Configuration Guide - AA Smart Organizer

## Overview

AA Smart Organizer uses a `config.json` file to determine which file types belong to which categories. This file is **fully customizable** without needing to edit any Python code!

---

## 🎯 Quick Start

### View Current Configuration

Open `config.json` in any text editor to see the current file type mappings.

### Reload Configuration

After editing `config.json`, click the **"🔄 Reload Config"** button in the app to apply changes without restarting.

---

## 📋 Default Categories

The default configuration includes **14 categories** with **100+ file types**:

| Category | File Types | Examples |
|----------|-----------|----------|
| 📄 **Documents** | 12 types | .pdf, .docx, .txt, .xlsx, .csv, .md |
| 🖼️ **Images** | 11 types | .jpg, .png, .gif, .svg, .heic, .raw |
| 🎥 **Videos** | 10 types | .mp4, .mkv, .avi, .mov, .3gp, .mts |
| 🎵 **Music** | 9 types | .mp3, .wav, .flac, .aac, .mid, .midi |
| ⚙️ **Installers** | 8 types | .exe, .msi, .dmg, .apk, .appimage |
| 📦 **Archives** | 8 types | .zip, .rar, .7z, .tar, .gz, .xz, .iso |
| 💻 **Code** | 17 types | .py, .js, .html, .css, .php, .ts, .yml |
| 🎮 **Game Files** | 12 types | .iso, .bin, .sav, .pak, .rom, .nes, .gba |
| 🖥️ **System** | 10 types | .bat, .cmd, .reg, .dll, .ini, .cfg, .log |
| 🎨 **Design** | 12 types | .psd, .ai, .xd, .fig, .blend, .fbx, .obj |
| 💾 **Backups** | 6 types | .img, .vhd, .vhdx, .bak, .gho, .tar.gz |
| 📚 **eBooks** | 6 types | .epub, .mobi, .azw3, .cbz, .cbr, .pdf |
| 🔌 **Plugins & Mods** | 8 types | .dll, .pak, .vst, .esp, .bsa, .mod, .asi |
| 📁 **Miscellaneous** | Empty | Catch-all for custom additions |

---

## ✏️ How to Customize

### 1. Add File Extensions to Existing Category

**Example:** Add `.numbers` to Documents

```json
{
    "file_types": {
        "Documents": [".pdf", ".docx", ".txt", ".numbers"],
        ...
    }
}
```

### 2. Remove File Extensions

**Example:** Remove `.log` files from System category

```json
{
    "file_types": {
        "System": [".bat", ".cmd", ".reg", ".dll", ".ini", ".cfg"],
        ...
    }
}
```

### 3. Create a New Category

**Example:** Add a "3D Models" category

```json
{
    "file_types": {
        "Documents": [".pdf", ".docx", ".txt"],
        "Images": [".jpg", ".png"],
        "3D Models": [".obj", ".fbx", ".stl", ".blend", ".3ds", ".dae"],
        ...
    }
}
```

### 4. Rename a Category

**Example:** Change "Music" to "Audio Files"

```json
{
    "file_types": {
        "Audio Files": [".mp3", ".wav", ".flac", ".aac"],
        ...
    }
}
```

### 5. Use Miscellaneous for Uncategorized Files

Add any file types you want organized but don't fit other categories:

```json
{
    "file_types": {
        "Miscellaneous": [".tmp", ".cache", ".bak", ".old"],
        ...
    }
}
```

---

## 🔄 Applying Changes

### Method 1: Hot Reload (Recommended)
1. Edit `config.json`
2. Save the file
3. Click **"🔄 Reload Config"** button in the app
4. Check the activity log for confirmation

### Method 2: Restart App
1. Edit `config.json`
2. Save the file
3. Close and restart the application

---

## 🛡️ Safety Features

### Auto-Validation
- Invalid JSON is automatically detected
- Corrupted configs are regenerated with defaults
- You'll see a warning in the activity log

### Auto-Regeneration
- Missing `config.json` is created automatically
- Default configuration with 14 categories
- No manual setup required

### Backward Compatibility
- Old config format (`"categories"`) is auto-migrated
- Seamless upgrade to new format (`"file_types"`)

---

## 💡 Tips & Best Practices

### ✅ Do's
- **Use lowercase** for all file extensions (e.g., `.pdf` not `.PDF`)
- **Include the dot** in extensions (e.g., `.txt` not `txt`)
- **Test changes** on a sample folder first
- **Backup** your custom config before major changes
- **Use descriptive names** for custom categories

### ❌ Don'ts
- **Don't remove** the `"file_types"` key
- **Don't use** special characters in category names (except spaces, &, -)
- **Don't duplicate** extensions across categories (first match wins)
- **Don't edit** while the app is organizing files

---

## 🧪 Testing Your Configuration

### Quick Test
1. Create a test folder with sample files
2. Add files with your custom extensions
3. Run organization
4. Check if files go to the correct categories

### Validation Checklist
- [ ] JSON syntax is valid (use a JSON validator)
- [ ] All extensions start with a dot (`.`)
- [ ] Category names are descriptive
- [ ] No duplicate extensions
- [ ] Tested with sample files

---

## 📖 Example Configurations

### Minimal Configuration
```json
{
    "file_types": {
        "Documents": [".pdf", ".txt", ".docx"],
        "Media": [".jpg", ".mp4", ".mp3"],
        "Other": [".zip", ".exe"]
    }
}
```

### Developer-Focused Configuration
```json
{
    "file_types": {
        "Python": [".py", ".pyw", ".pyc"],
        "JavaScript": [".js", ".jsx", ".ts", ".tsx"],
        "Web": [".html", ".css", ".scss"],
        "Data": [".json", ".xml", ".yaml", ".csv"],
        "Docs": [".md", ".txt", ".pdf"]
    }
}
```

### Media Professional Configuration
```json
{
    "file_types": {
        "Raw Photos": [".raw", ".cr2", ".nef", ".arw"],
        "Edited Photos": [".jpg", ".png", ".tiff"],
        "Video Projects": [".prproj", ".aep", ".fcpx"],
        "Video Exports": [".mp4", ".mov", ".avi"],
        "Audio": [".wav", ".mp3", ".aac"]
    }
}
```

### Gamer Configuration
```json
{
    "file_types": {
        "Game Installers": [".exe", ".msi"],
        "Game ISOs": [".iso", ".bin", ".cue"],
        "Save Files": [".sav", ".dat", ".save"],
        "Mods": [".pak", ".mod", ".esp", ".bsa"],
        "ROMs": [".rom", ".nes", ".gba", ".n64"]
    }
}
```

---

## 🐛 Troubleshooting

### Config Not Loading
**Problem:** Changes not appearing after reload  
**Solution:** 
- Check JSON syntax with a validator
- Look for error messages in activity log
- Restart the app if reload doesn't work

### Files Not Organizing
**Problem:** Files not moving to expected category  
**Solution:**
- Verify extension is in `config.json`
- Check extension is lowercase
- Ensure extension includes the dot (`.`)

### Config Keeps Resetting
**Problem:** Config reverts to defaults  
**Solution:**
- Check file permissions (read/write access)
- Ensure JSON is valid
- Don't edit while app is running

### Category Not Created
**Problem:** New category folder not appearing  
**Solution:**
- Ensure at least one file matches the category
- Check that category name is valid
- Reload config after editing

---

## 🔧 Advanced Usage

### Multiple Extensions for Same File Type

Some file types have multiple extensions:

```json
{
    "file_types": {
        "Images": [".jpg", ".jpeg", ".png"],
        "Archives": [".tar.gz", ".tar", ".gz"]
    }
}
```

### Empty Categories

Use empty arrays for categories you might use later:

```json
{
    "file_types": {
        "Future Category": []
    }
}
```

### Special Characters in Names

Category names can include:
- Spaces: `"3D Models"`
- Ampersands: `"Plugins & Mods"`
- Hyphens: `"Work-Related"`

---

## 📞 Support

If you need help customizing your configuration:
1. Check this guide
2. Review the activity log for error messages
3. Test with the default config first
4. Contact **AA's Computer and Remote Services**

---

**Made with ❤️ by AA's Computer and Remote Services**
