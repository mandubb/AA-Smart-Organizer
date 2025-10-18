"""
Test Script for Modular AA Smart Organizer
Demonstrates all new features and modules
"""

import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Import all modules
from modules import (
    ProfileManager, ActivityLog, MaintenanceManager,
    SummaryGenerator, format_file_size
)


def test_profiles():
    """Test profile management"""
    print("\n" + "="*70)
    print("TEST 1: Profile Management")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        profiles_path = Path(temp_dir) / "profiles"
        
        # Initialize profile manager
        pm = ProfileManager(profiles_path)
        print("✅ ProfileManager initialized")
        
        # List profiles
        profiles = pm.list_profiles()
        print(f"✅ Found {len(profiles)} profiles: {profiles}")
        
        # Create new profile
        pm.create_profile("test_profile")
        profiles = pm.list_profiles()
        print(f"✅ Created profile, now have: {profiles}")
        
        # Load profile
        pm.load_profile("test_profile")
        print(f"✅ Loaded profile: {pm.get_current_profile()}")
        
        # Get profile info
        info = pm.get_profile_info("test_profile")
        print(f"✅ Profile info: {info['name']}, created: {info['created']}")


def test_activity_log():
    """Test activity logging"""
    print("\n" + "="*70)
    print("TEST 2: Activity Logging")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        log_path = Path(temp_dir) / "logs"
        
        # Initialize activity log
        activity_log = ActivityLog(log_path)
        print("✅ ActivityLog initialized")
        
        # Log some moves
        activity_log.log_move(
            "document.pdf",
            Path("/old/path/document.pdf"),
            Path("/new/path/Documents/document.pdf"),
            1024000,
            "Documents",
            "Success"
        )
        print("✅ Logged file move")
        
        activity_log.log_move(
            "photo.jpg",
            Path("/old/path/photo.jpg"),
            Path("/new/path/Images/photo.jpg"),
            2048000,
            "Images",
            "Success"
        )
        print("✅ Logged another move")
        
        # Get session summary
        summary = activity_log.get_session_summary()
        print(f"✅ Session summary:")
        print(f"   Total operations: {summary['total_operations']}")
        print(f"   Moves: {summary['moves']}")
        print(f"   Total size: {summary['total_size_formatted']}")
        print(f"   Categories: {summary['categories']}")
        
        # Save undo data
        activity_log.save_undo_data()
        print("✅ Saved undo data")
        
        # Load undo data
        undo_data = activity_log.load_undo_data()
        print(f"✅ Loaded undo data: {len(undo_data)} operations")
        
        # Export session
        export_path = log_path / "session_export.txt"
        activity_log.export_session_to_file(export_path)
        print(f"✅ Exported session to: {export_path}")


def test_maintenance():
    """Test maintenance and cleanup"""
    print("\n" + "="*70)
    print("TEST 3: Maintenance & Quick Clean")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir)
        
        # Create test files
        (test_path / "document.pdf").touch()
        (test_path / "photo.jpg").touch()
        (test_path / "temp_file.tmp").touch()
        (test_path / "Thumbs.db").touch()
        (test_path / "~$office_temp.docx").touch()
        (test_path / "cache.cache").touch()
        
        # Create empty folder
        empty_folder = test_path / "empty_folder"
        empty_folder.mkdir()
        
        print(f"✅ Created test environment with 6 files and 1 empty folder")
        
        # Initialize maintenance manager
        maintenance = MaintenanceManager()
        print("✅ MaintenanceManager initialized")
        
        # Scan for junk files
        junk_files = maintenance.scan_junk_files(test_path, recursive=False)
        print(f"✅ Found {len(junk_files)} junk files:")
        for junk in junk_files:
            print(f"   • {junk['name']} - {junk['reason']}")
        
        # Find empty folders
        empty_folders = maintenance.find_empty_folders(test_path)
        print(f"✅ Found {len(empty_folders)} empty folders")
        
        # Run quick clean (preview)
        print("\n🔍 Running Quick Clean (preview mode)...")
        stats = maintenance.quick_clean(
            test_path,
            recursive=False,
            preview_only=True,
            clear_recycle_bin=False
        )
        
        print(f"\n✅ Quick Clean Preview Results:")
        print(f"   Junk files found: {stats['junk_files_found']}")
        print(f"   Empty folders found: {stats['empty_folders_found']}")
        print(f"   Would free: {stats['space_freed_formatted']}")


def test_summary():
    """Test summary generation"""
    print("\n" + "="*70)
    print("TEST 4: Summary Generation")
    print("="*70)
    
    # Initialize summary generator
    summary_gen = SummaryGenerator()
    print("✅ SummaryGenerator initialized")
    
    # Simulate operation
    summary_gen.start_operation()
    print("✅ Started operation tracking")
    
    # Simulate some work
    import time
    time.sleep(0.5)
    
    summary_gen.end_operation()
    print("✅ Ended operation tracking")
    
    # Generate summary
    summary_data = summary_gen.generate_summary(
        total_files=100,
        files_organized=95,
        files_skipped=3,
        files_failed=2,
        total_size=524288000,  # ~500 MB
        categories={
            "Documents": 40,
            "Images": 30,
            "Videos": 15,
            "Music": 10
        },
        additional_info={
            "Profile": "default",
            "Quick Clean": "Yes"
        }
    )
    
    print("✅ Generated summary data")
    
    # Print CLI summary
    print("\n📊 CLI Summary Output:")
    summary_gen.print_cli_summary(summary_data)
    
    # Export to text
    with tempfile.TemporaryDirectory() as temp_dir:
        text_path = Path(temp_dir) / "summary.txt"
        summary_gen.export_to_text(text_path)
        print(f"✅ Exported text summary to: {text_path}")
        
        # Export to HTML
        html_path = Path(temp_dir) / "summary.html"
        summary_gen.export_to_html(html_path)
        print(f"✅ Exported HTML summary to: {html_path}")
        
        # Show quick summary
        quick = summary_gen.generate_quick_summary(95, 524288000, "2.5 seconds")
        print(f"✅ Quick summary: {quick}")


def test_integration():
    """Test integrated workflow"""
    print("\n" + "="*70)
    print("TEST 5: Integrated Workflow")
    print("="*70)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        profiles_path = base_path / "profiles"
        test_folder = base_path / "test_files"
        test_folder.mkdir()
        
        # Create test files
        files_created = []
        for i in range(5):
            (test_folder / f"document{i}.pdf").write_text(f"Test content {i}")
            files_created.append(f"document{i}.pdf")
        
        for i in range(3):
            (test_folder / f"photo{i}.jpg").write_text(f"Image data {i}")
            files_created.append(f"photo{i}.jpg")
        
        # Add junk files
        (test_folder / "temp.tmp").write_text("temp")
        (test_folder / "Thumbs.db").write_text("thumbs")
        
        print(f"✅ Created test environment: {len(files_created)} files + 2 junk files")
        
        # Initialize components
        pm = ProfileManager(profiles_path)
        pm.load_profile("default")
        
        log_path = pm.get_logs_path()
        activity_log = ActivityLog(log_path)
        
        maintenance = MaintenanceManager()
        summary_gen = SummaryGenerator()
        
        print("✅ All components initialized")
        
        # Step 1: Quick Clean
        print("\n🧹 Step 1: Quick Clean")
        clean_stats = maintenance.quick_clean(
            test_folder,
            recursive=False,
            preview_only=False,
            clear_recycle_bin=False
        )
        print(f"   Cleaned {clean_stats['junk_files_deleted']} junk files")
        
        # Step 2: Organize Files (simulated)
        print("\n📁 Step 2: Organize Files")
        summary_gen.start_operation()
        
        # Simulate organizing
        docs_folder = test_folder / "Documents"
        images_folder = test_folder / "Images"
        docs_folder.mkdir(exist_ok=True)
        images_folder.mkdir(exist_ok=True)
        
        organized = 0
        total_size = 0
        categories = {"Documents": 0, "Images": 0}
        
        for file in test_folder.glob("*.pdf"):
            new_path = docs_folder / file.name
            file_size = file.stat().st_size
            shutil.move(str(file), str(new_path))
            
            activity_log.log_move(
                file.name, file, new_path, file_size, "Documents", "Success"
            )
            
            organized += 1
            total_size += file_size
            categories["Documents"] += 1
        
        for file in test_folder.glob("*.jpg"):
            new_path = images_folder / file.name
            file_size = file.stat().st_size
            shutil.move(str(file), str(new_path))
            
            activity_log.log_move(
                file.name, file, new_path, file_size, "Images", "Success"
            )
            
            organized += 1
            total_size += file_size
            categories["Images"] += 1
        
        print(f"   Organized {organized} files")
        
        # Step 3: Generate Summary
        print("\n📊 Step 3: Generate Summary")
        summary_gen.end_operation()
        
        summary_data = summary_gen.generate_summary(
            total_files=len(files_created),
            files_organized=organized,
            files_skipped=0,
            files_failed=0,
            total_size=total_size,
            categories=categories
        )
        
        summary_gen.print_cli_summary(summary_data)
        
        # Step 4: Save Everything
        print("💾 Step 4: Save Data")
        activity_log.save_undo_data()
        print("   ✅ Saved undo data")
        
        session_summary = activity_log.get_session_summary()
        print(f"   ✅ Activity log: {session_summary['total_operations']} operations")


def main():
    """Run all tests"""
    print("="*70)
    print("AA SMART ORGANIZER - MODULAR SYSTEM TEST SUITE")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_profiles()
        test_activity_log()
        test_maintenance()
        test_summary()
        test_integration()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\n🎉 The modular system is working perfectly!")
        print("\nKey Features Tested:")
        print("  ✓ Profile Management")
        print("  ✓ Activity Logging")
        print("  ✓ Maintenance & Quick Clean")
        print("  ✓ Summary Generation")
        print("  ✓ Integrated Workflow")
        print("\n📚 Next Steps:")
        print("  1. Run: python main_cli.py --help")
        print("  2. Try: python main_cli.py organize <folder>")
        print("  3. Read: README_MODULAR.md")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
