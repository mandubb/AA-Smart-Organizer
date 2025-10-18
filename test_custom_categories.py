"""
Test script to verify custom category functionality
Demonstrates that users can add custom categories without modifying code
"""

import json
import os
import tempfile
import shutil
from pathlib import Path
from organizer import FileOrganizer


def test_custom_categories():
    """Test that custom categories work correctly"""
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a custom config.json with user-added categories
        config_path = temp_path / "config.json"
        custom_config = {
            "file_types": {
                # Standard categories
                "Documents": [".pdf", ".docx", ".txt"],
                "Images": [".jpg", ".png"],
                
                # User-added custom categories
                "Blender Projects": [".blend", ".blend1"],
                "CAD Files": [".dwg", ".dxf", ".step", ".stp"],
                "My Custom Files": [".custom", ".xyz"],
                "3D Printing": [".stl", ".obj", ".gcode"],
                
                # Empty category (should still work)
                "Future Category": []
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(custom_config, f, indent=4)
        
        print("✅ Created custom config.json with user categories")
        print(f"   Categories: {list(custom_config['file_types'].keys())}")
        
        # Create test files
        test_files = [
            "document.pdf",
            "photo.jpg",
            "model.blend",
            "design.dwg",
            "data.custom",
            "print.stl",
            "unknown.zzz"  # This won't be organized
        ]
        
        for filename in test_files:
            (temp_path / filename).touch()
        
        print(f"\n✅ Created {len(test_files)} test files")
        
        # Initialize organizer with custom config
        organizer = FileOrganizer(
            config_file=str(config_path),
            log_callback=lambda msg: print(f"   {msg}")
        )
        
        print("\n📊 Organizer initialized with categories:")
        for category in organizer.get_categories_list():
            print(f"   • {category}")
        
        # Verify custom categories were loaded
        assert "Blender Projects" in organizer.categories, "Custom category 'Blender Projects' not loaded"
        assert "CAD Files" in organizer.categories, "Custom category 'CAD Files' not loaded"
        assert "My Custom Files" in organizer.categories, "Custom category 'My Custom Files' not loaded"
        assert "3D Printing" in organizer.categories, "Custom category '3D Printing' not loaded"
        
        print("\n✅ All custom categories loaded successfully!")
        
        # Test file categorization
        test_cases = [
            (".blend", "Blender Projects"),
            (".dwg", "CAD Files"),
            (".custom", "My Custom Files"),
            (".stl", "3D Printing"),
            (".pdf", "Documents"),
            (".jpg", "Images"),
        ]
        
        print("\n🔍 Testing file categorization:")
        for ext, expected_category in test_cases:
            category = organizer.get_category(ext)
            assert category == expected_category, f"Extension {ext} should be in '{expected_category}', got '{category}'"
            print(f"   ✓ {ext} → {category}")
        
        # Organize the files
        print("\n🚀 Organizing files...")
        stats = organizer.organize_folder(temp_path)
        
        print("\n📊 Organization results:")
        for category, count in stats.items():
            print(f"   • {category}: {count} files")
        
        # Verify folders were created
        print("\n📁 Created folders:")
        for category in stats.keys():
            folder_path = temp_path / category
            assert folder_path.exists(), f"Folder '{category}' was not created"
            print(f"   ✓ {category}/")
        
        # Verify files were moved correctly
        print("\n✅ Verifying file locations:")
        expected_moves = {
            "document.pdf": "Documents",
            "photo.jpg": "Images",
            "model.blend": "Blender Projects",
            "design.dwg": "CAD Files",
            "data.custom": "My Custom Files",
            "print.stl": "3D Printing"
        }
        
        for filename, expected_folder in expected_moves.items():
            expected_path = temp_path / expected_folder / filename
            assert expected_path.exists(), f"{filename} not found in {expected_folder}/"
            print(f"   ✓ {filename} → {expected_folder}/")
        
        # Verify unorganized file stayed in root
        assert (temp_path / "unknown.zzz").exists(), "Unknown file should remain in root"
        print(f"   ✓ unknown.zzz → (stayed in root)")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n🎉 Custom categories work perfectly!")
        print("   Users can add any category to config.json without code changes.")


def test_invalid_categories():
    """Test that invalid categories are handled gracefully"""
    
    print("\n" + "="*60)
    print("Testing invalid category handling...")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config_path = temp_path / "config.json"
        
        # Create config with some invalid entries
        invalid_config = {
            "file_types": {
                "Valid Category": [".valid"],
                "Invalid Extensions": "not a list",  # Invalid: not a list
                "": [".empty"],  # Invalid: empty name
                "Mixed Valid": [".good", 123, ".also_good"],  # Partially valid
                "Another Valid": [".another"]
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(invalid_config, f, indent=4)
        
        print("\n📝 Created config with invalid entries")
        
        # Initialize organizer - should skip invalid entries
        messages = []
        organizer = FileOrganizer(
            config_file=str(config_path),
            log_callback=lambda msg: messages.append(msg)
        )
        
        print("\n📋 Log messages:")
        for msg in messages:
            print(f"   {msg}")
        
        # Verify valid categories were loaded
        assert "Valid Category" in organizer.categories
        assert "Another Valid" in organizer.categories
        assert "Mixed Valid" in organizer.categories
        
        # Verify invalid categories were skipped
        assert "Invalid Extensions" not in organizer.categories
        assert "" not in organizer.categories
        
        # Verify Mixed Valid has only valid extensions
        assert ".good" in organizer.categories["Mixed Valid"]
        assert ".also_good" in organizer.categories["Mixed Valid"]
        assert 123 not in organizer.categories["Mixed Valid"]
        
        print("\n✅ Invalid categories handled gracefully!")
        print(f"   Loaded {len(organizer.categories)} valid categories")


if __name__ == "__main__":
    print("="*60)
    print("AA Smart Organizer - Custom Categories Test")
    print("="*60)
    
    try:
        test_custom_categories()
        test_invalid_categories()
        
        print("\n" + "="*60)
        print("🎊 ALL TESTS COMPLETED SUCCESSFULLY! 🎊")
        print("="*60)
        print("\n💡 Users can now:")
        print("   1. Add custom categories to config.json")
        print("   2. Define custom file extensions")
        print("   3. Folders are created automatically during organization")
        print("   4. Invalid entries are skipped with warnings")
        print("   5. No code changes needed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        raise
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
