"""
Test script to verify AA Smart Organizer functionality
Creates a test folder with sample files and tests the organizer
"""

import os
import shutil
from pathlib import Path
from organizer import FileOrganizer
from undo_manager import UndoManager


def create_test_folder():
    """Create a test folder with sample files"""
    test_folder = Path("test_messy_folder")
    
    # Remove if exists
    if test_folder.exists():
        shutil.rmtree(test_folder)
    
    # Create folder
    test_folder.mkdir()
    
    # Create sample files
    sample_files = [
        "document1.pdf",
        "document2.docx",
        "report.txt",
        "image1.jpg",
        "image2.png",
        "photo.jpeg",
        "video1.mp4",
        "video2.mkv",
        "song1.mp3",
        "song2.wav",
        "installer.exe",
        "setup.msi",
        "archive.zip",
        "code.py",
        "script.js",
        "readme.md"
    ]
    
    for filename in sample_files:
        file_path = test_folder / filename
        file_path.write_text(f"Test content for {filename}")
    
    print(f"✅ Created test folder with {len(sample_files)} files")
    return test_folder


def test_organizer():
    """Test the file organizer"""
    print("\n" + "="*60)
    print("🧪 Testing AA Smart Organizer")
    print("="*60)
    
    # Create test folder
    test_folder = create_test_folder()
    
    # Initialize organizer and undo manager
    organizer = FileOrganizer()
    undo_manager = UndoManager("test_undo_log.json")
    
    # Test 1: Get organizable count
    print("\n📊 Test 1: Checking file counts...")
    total, organizable = organizer.get_organizable_count(test_folder)
    print(f"   Total files: {total}")
    print(f"   Organizable files: {organizable}")
    assert total > 0, "Should have files in test folder"
    assert organizable > 0, "Should have organizable files"
    print("   ✅ File count test passed")
    
    # Test 2: Organize files
    print("\n🗂️ Test 2: Organizing files...")
    
    def progress_callback(current, total, filename):
        print(f"   Processing: {filename} ({current}/{total})")
    
    stats = organizer.organize_folder(
        test_folder,
        progress_callback=progress_callback,
        undo_manager=undo_manager
    )
    
    print(f"\n   Organization results:")
    for category, count in stats.items():
        print(f"   • {category}: {count} files")
    
    total_moved = sum(stats.values())
    assert total_moved > 0, "Should have moved some files"
    print(f"   ✅ Successfully organized {total_moved} files")
    
    # Save undo session
    undo_manager.save_session()
    
    # Test 3: Verify folders were created
    print("\n📁 Test 3: Verifying category folders...")
    for category in stats.keys():
        category_folder = test_folder / category
        assert category_folder.exists(), f"{category} folder should exist"
        files_in_category = list(category_folder.glob("*"))
        print(f"   • {category}: {len(files_in_category)} files")
    print("   ✅ All category folders verified")
    
    # Test 4: Undo operation
    print("\n↶ Test 4: Testing undo functionality...")
    success, message, count = undo_manager.undo_last_session()
    assert success, "Undo should succeed"
    assert count > 0, "Should have restored files"
    print(f"   {message}")
    print(f"   ✅ Successfully restored {count} files")
    
    # Test 5: Verify files are back
    print("\n🔍 Test 5: Verifying files restored...")
    files_in_root = [f for f in test_folder.iterdir() if f.is_file()]
    print(f"   Files in root folder: {len(files_in_root)}")
    assert len(files_in_root) > 0, "Files should be restored to root"
    print("   ✅ Files successfully restored")
    
    # Cleanup
    print("\n🧹 Cleaning up test files...")
    shutil.rmtree(test_folder)
    if os.path.exists("test_undo_log.json"):
        os.remove("test_undo_log.json")
    print("   ✅ Cleanup complete")
    
    print("\n" + "="*60)
    print("🎉 All tests passed successfully!")
    print("="*60)
    print("\n✅ AA Smart Organizer is ready to use!")
    print("   Run 'python main.py' to launch the GUI application")


if __name__ == "__main__":
    try:
        test_organizer()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
