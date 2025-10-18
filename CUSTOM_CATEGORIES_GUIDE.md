# Custom Categories Guide

## 🎯 Overview

AA Smart Organizer is fully user-customizable! You can add, edit, or remove file categories directly in `config.json` without modifying any Python code.

## 📝 How to Add Custom Categories

### Step 1: Open config.json

Open the `config.json` file in any text editor. You'll see a structure like this:

```json
{
    "file_types": {
        "Documents": [".pdf", ".docx", ".txt"],
        "Images": [".jpg", ".png", ".gif"],
        "Videos": [".mp4", ".mkv", ".avi"]
    }
}
```

### Step 2: Add Your Custom Category

Simply add a new entry with your category name and file extensions:

```json
{
    "file_types": {
        "Documents": [".pdf", ".docx", ".txt"],
        "Images": [".jpg", ".png", ".gif"],
        "Videos": [".mp4", ".mkv", ".avi"],
        
        "Blender Projects": [".blend", ".blend1"],
        "CAD Files": [".dwg", ".dxf", ".step", ".stp"],
        "My Custom Files": [".custom", ".xyz"]
    }
}
```

### Step 3: Save and Reload

1. Save the `config.json` file
2. In the app, click the **"🔄 Reload Config"** button
3. Your new categories are now active!

## ✅ Requirements

### Category Names
- Must be a **string** (text)
- Cannot be empty
- Can contain spaces and special characters
- Examples: `"3D Models"`, `"Client Files - 2024"`, `"My_Projects"`

### File Extensions
- Must be a **list** (array) of strings
- Each extension should start with a dot (`.`)
- Extensions are case-insensitive (`.PDF` = `.pdf`)
- Can be an empty list `[]` for future use
- Examples: `[".blend"]`, `[".dwg", ".dxf"]`, `[]`

## 📋 Valid Configuration Examples

### Example 1: Creative Professional

```json
{
    "file_types": {
        "Photoshop Projects": [".psd", ".psb"],
        "Blender Files": [".blend", ".blend1"],
        "CAD Drawings": [".dwg", ".dxf", ".dwf"],
        "3D Prints": [".stl", ".obj", ".gcode"],
        "Video Projects": [".prproj", ".aep"],
        "Audio Samples": [".wav", ".aiff", ".flac"]
    }
}
```

### Example 2: Developer

```json
{
    "file_types": {
        "Python Projects": [".py", ".pyc", ".pyw"],
        "JavaScript": [".js", ".jsx", ".ts", ".tsx"],
        "Web Files": [".html", ".css", ".scss"],
        "Config Files": [".json", ".yaml", ".yml", ".toml"],
        "Database": [".db", ".sqlite", ".sql"],
        "Documentation": [".md", ".rst", ".txt"]
    }
}
```

### Example 3: Student/Academic

```json
{
    "file_types": {
        "Assignments": [".docx", ".pdf", ".txt"],
        "Presentations": [".pptx", ".ppt"],
        "Spreadsheets": [".xlsx", ".xls", ".csv"],
        "Research Papers": [".pdf", ".tex"],
        "Code Projects": [".py", ".java", ".cpp"],
        "Lab Data": [".csv", ".dat", ".mat"]
    }
}
```

## ⚠️ Invalid Configurations (Will Be Skipped)

### ❌ Extensions Not a List
```json
"My Category": ".txt"  // Wrong! Must be a list
```
**Correct:**
```json
"My Category": [".txt"]
```

### ❌ Empty Category Name
```json
"": [".txt"]  // Wrong! Category name cannot be empty
```

### ❌ Non-String Extensions
```json
"My Category": [".txt", 123, true]  // Wrong! Only strings allowed
```
**Correct:**
```json
"My Category": [".txt"]  // Numbers and booleans will be skipped
```

## 🔄 How It Works

1. **Dynamic Loading**: The app reads all categories from `config.json` at startup
2. **Automatic Folder Creation**: When organizing, folders are created automatically for each category that has files
3. **Validation**: Invalid entries are logged as warnings but don't break the app
4. **Graceful Skipping**: Files with extensions not in any category remain in the root folder

## 🎯 Real-World Example

Let's say you're a game developer and want to organize your project files:

```json
{
    "file_types": {
        "Unity Projects": [".unity", ".prefab", ".asset"],
        "Unreal Projects": [".uproject", ".uasset"],
        "3D Models": [".fbx", ".obj", ".blend"],
        "Textures": [".png", ".jpg", ".tga", ".dds"],
        "Audio": [".wav", ".ogg", ".mp3"],
        "Scripts": [".cs", ".cpp", ".h", ".py"],
        "Game Builds": [".exe", ".apk", ".ipa"],
        "Documentation": [".md", ".pdf", ".txt"]
    }
}
```

When you organize a folder with these files:
- `PlayerController.cs` → **Scripts/**
- `MainMenu.unity` → **Unity Projects/**
- `Character.fbx` → **3D Models/**
- `Background.png` → **Textures/**
- `Footstep.wav` → **Audio/**
- `Game.exe` → **Game Builds/**
- `README.md` → **Documentation/**

## 🛡️ Safety Features

1. **Validation**: Invalid categories are skipped with warnings
2. **Preservation**: User categories are preserved even if config regenerates
3. **No Data Loss**: Files that don't match any category stay in place
4. **Duplicate Handling**: Files with duplicate names get numbered (e.g., `file_1.txt`)
5. **Undo Support**: You can undo any organization operation

## 💡 Tips

1. **Use Descriptive Names**: `"Client Projects 2024"` is better than `"Misc"`
2. **Group Related Extensions**: Put all video formats in one category
3. **Empty Categories**: You can create categories with `[]` for future use
4. **Reload After Changes**: Always click "🔄 Reload Config" after editing
5. **Test First**: Try organizing a test folder before your important files

## 🔧 Troubleshooting

### Category Not Working?
1. Check that extensions start with a dot (`.blend` not `blend`)
2. Ensure the category name is not empty
3. Verify the JSON syntax is valid (use a JSON validator)
4. Click "🔄 Reload Config" after making changes

### Files Not Being Organized?
1. Check if the file extension is in any category
2. Verify the extension matches exactly (case-insensitive)
3. Look at the Activity Log for warnings

### Config File Corrupted?
Don't worry! The app will regenerate it with defaults and try to preserve your custom categories.

## 📚 Additional Resources

- See `test_custom_categories.py` for working examples
- Check the Activity Log in the app for validation messages
- Default categories are in `organizer.py` (for reference only)

---

**Made with ❤️ by AA's Computer and Remote Services**
