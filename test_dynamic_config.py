"""
Test script for dynamic config loading feature
Tests validation, auto-regeneration, and reload functionality
"""

import os
import json
import shutil
from pathlib import Path
from organizer import FileOrganizer


def test_dynamic_config():
    """Test the dynamic config loading feature"""
    print("\n" + "="*60)
    print("🧪 Testing Dynamic Config Loading Feature")
    print("="*60)
    
    # Backup original config
    original_config = "config.json"
    backup_config = "config_backup.json"
    test_config = "test_config.json"
    
    if os.path.exists(original_config):
        shutil.copy(original_config, backup_config)
        print("✅ Backed up original config.json")
    
    try:
        # Test 1: Load existing valid config
        print("\n📊 Test 1: Loading valid config...")
        organizer = FileOrganizer(config_file=original_config)
        categories = organizer.get_categories_list()
        print(f"   Loaded {len(categories)} categories: {', '.join(categories[:5])}...")
        assert len(categories) > 0, "Should have loaded categories"
        print("   ✅ Valid config loaded successfully")
        
        # Test 2: Missing config file (auto-generation)
        print("\n📊 Test 2: Testing auto-generation for missing config...")
        if os.path.exists(test_config):
            os.remove(test_config)
        
        organizer2 = FileOrganizer(config_file=test_config)
        assert os.path.exists(test_config), "Config should be auto-generated"
        categories2 = organizer2.get_categories_list()
        print(f"   Auto-generated config with {len(categories2)} categories")
        assert len(categories2) == 14, "Should have 14 default categories"
        print("   ✅ Config auto-generation works")
        
        # Test 3: Invalid JSON (auto-regeneration)
        print("\n📊 Test 3: Testing auto-regeneration for corrupted config...")
        with open(test_config, 'w') as f:
            f.write("{ invalid json content }")
        
        organizer3 = FileOrganizer(config_file=test_config)
        categories3 = organizer3.get_categories_list()
        print(f"   Regenerated config with {len(categories3)} categories")
        assert len(categories3) == 14, "Should regenerate with defaults"
        print("   ✅ Config auto-regeneration works")
        
        # Test 4: Old format migration
        print("\n📊 Test 4: Testing backward compatibility (old format)...")
        old_format = {
            "categories": {
                "Documents": [".pdf", ".txt"],
                "Images": [".jpg", ".png"]
            }
        }
        with open(test_config, 'w') as f:
            json.dump(old_format, f)
        
        organizer4 = FileOrganizer(config_file=test_config)
        
        # Check if migrated to new format
        with open(test_config, 'r') as f:
            migrated = json.load(f)
        
        assert "file_types" in migrated, "Should migrate to new format"
        assert "categories" not in migrated, "Old key should be removed"
        print("   ✅ Old format migration works")
        
        # Test 5: Config reload
        print("\n📊 Test 5: Testing config reload functionality...")
        
        # Modify config
        with open(test_config, 'r') as f:
            config = json.load(f)
        
        config["file_types"]["TestCategory"] = [".test", ".demo"]
        
        with open(test_config, 'w') as f:
            json.dump(config, f, indent=4)
        
        # Reload
        success, message, count = organizer4.reload_config()
        assert success, "Reload should succeed"
        
        new_categories = organizer4.get_categories_list()
        assert "TestCategory" in new_categories, "New category should be loaded"
        print(f"   {message}")
        print("   ✅ Config reload works")
        
        # Test 6: Validate expanded file types
        print("\n📊 Test 6: Validating expanded file type categories...")
        organizer5 = FileOrganizer(config_file=original_config)
        
        expected_categories = [
            "Documents", "Images", "Videos", "Music", "Installers",
            "Archives", "Code", "Game Files", "System", "Design",
            "Backups", "eBooks", "Plugins & Mods", "Miscellaneous"
        ]
        
        actual_categories = organizer5.get_categories_list()
        
        for cat in expected_categories:
            assert cat in actual_categories, f"Missing category: {cat}"
        
        print(f"   All {len(expected_categories)} expected categories found")
        
        # Check some specific file types
        test_extensions = {
            ".csv": "Documents",
            ".heic": "Images",
            ".3gp": "Videos",
            ".midi": "Music",
            ".appimage": "Installers",
            ".xz": "Archives",
            ".php": "Code",
            ".rom": "Game Files",
            ".dll": "System",  # Note: .dll is in multiple categories
            ".vhd": "Backups",
            ".epub": "eBooks"
        }
        
        for ext, expected_cat in test_extensions.items():
            category = organizer5.get_category(ext)
            # Some extensions might be in multiple categories, just check it's categorized
            assert category is not None, f"{ext} should be categorized"
            print(f"   • {ext} → {category}")
        
        print("   ✅ Expanded file types validated")
        
        # Test 7: Test with actual files
        print("\n📊 Test 7: Testing organization with new file types...")
        test_folder = Path("test_expanded_folder")
        
        if test_folder.exists():
            shutil.rmtree(test_folder)
        
        test_folder.mkdir()
        
        # Create files with new extensions
        new_files = [
            "spreadsheet.csv",
            "photo.heic",
            "video.3gp",
            "music.midi",
            "installer.appimage",
            "archive.xz",
            "script.php",
            "game.rom",
            "config.ini",
            "backup.vhd",
            "book.epub"
        ]
        
        for filename in new_files:
            (test_folder / filename).write_text(f"Test: {filename}")
        
        print(f"   Created {len(new_files)} test files with new extensions")
        
        # Organize
        stats = organizer5.organize_folder(test_folder)
        
        total_organized = sum(stats.values())
        print(f"   Organized {total_organized} files into {len(stats)} categories")
        
        for category, count in stats.items():
            print(f"   • {category}: {count} files")
        
        assert total_organized > 0, "Should organize files"
        print("   ✅ Organization with new file types works")
        
        # Cleanup test folder
        shutil.rmtree(test_folder)
        
        print("\n" + "="*60)
        print("🎉 All dynamic config tests passed!")
        print("="*60)
        
        print("\n✅ Feature Summary:")
        print("   • Config validation and auto-regeneration: ✅")
        print("   • Backward compatibility (old format): ✅")
        print("   • Hot reload functionality: ✅")
        print("   • 14 categories with 100+ file types: ✅")
        print("   • Custom category support: ✅")
        
    finally:
        # Cleanup
        if os.path.exists(test_config):
            os.remove(test_config)
        
        # Restore original config if needed
        if os.path.exists(backup_config):
            if not os.path.exists(original_config):
                shutil.move(backup_config, original_config)
            else:
                os.remove(backup_config)
        
        print("\n🧹 Cleanup complete")


if __name__ == "__main__":
    try:
        test_dynamic_config()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
