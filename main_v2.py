"""
AA Smart Organizer
Modern desktop app with dark futuristic theme, PDF export, and enhanced safety
"""

import os
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox
from datetime import datetime
import customtkinter as ctk

# Import our modules
from organizer import FileOrganizer
from undo_manager import UndoManager
from modules import (
    ActivityLog, MaintenanceManager,
    SummaryGenerator, format_file_size
)
from modules.gui_futuristic import show_clean_confirmation_dialog, FuturisticTheme


class AASmartOrganizerV3(ctk.CTk):
    """Main application window with futuristic features"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("⚡ AA Smart Organizer")
        self.geometry("1200x800")
        self.resizable(True, True)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize paths (no profiles - single global config)
        self.base_path = Path(__file__).parent
        self.config_path = self.base_path / "config.json"
        self.logs_path = self.base_path / "logs"
        self.exports_path = self.base_path / "exports" / "summaries"
        
        # Ensure directories exist
        self.logs_path.mkdir(exist_ok=True)
        self.exports_path.mkdir(parents=True, exist_ok=True)
        
        self.activity_log = None
        self.maintenance = None
        self.summary = None
        
        # Initialize traditional components
        self.undo_manager = UndoManager()
        self.selected_folder = None
        self.is_organizing = False
        self.organizer = None
        
        # Create UI
        self._create_ui()
        
        # Initialize components with log callback
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all components"""
        # Initialize organizer with global config
        self.organizer = FileOrganizer(
            config_file=str(self.config_path),
            log_callback=self._log_message
        )
        
        # Initialize activity log
        self.activity_log = ActivityLog(self.logs_path)
        
        # Initialize maintenance
        self.maintenance = MaintenanceManager(log_callback=self._log_message)
        
        # Initialize summary
        self.summary = SummaryGenerator()
        
        self._log_message("✅ AA Smart Organizer loaded")
    
    def _create_ui(self):
        """Build the user interface"""
        
        # Title Section
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=(15, 10), padx=20, fill="x")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="⚡ AA Smart Organizer",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=FuturisticTheme.ACCENT_CYAN
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Automate Smarter",
            font=ctk.CTkFont(size=11),
            text_color=FuturisticTheme.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Folder Selection Section
        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(pady=10, padx=20, fill="x")
        
        folder_label = ctk.CTkLabel(
            folder_frame,
            text="Select Folder to Organize:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        folder_label.pack(pady=(15, 10), padx=15, anchor="w")
        
        # Folder path display and browse button
        path_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
        path_frame.pack(pady=(0, 15), padx=15, fill="x")
        
        self.folder_path_var = ctk.StringVar(value="No folder selected")
        self.folder_path_label = ctk.CTkLabel(
            path_frame,
            textvariable=self.folder_path_var,
            font=ctk.CTkFont(size=11),
            anchor="w",
            fg_color=("gray85", "gray25"),
            corner_radius=6,
            height=35
        )
        self.folder_path_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.browse_button = ctk.CTkButton(
            path_frame,
            text="📁 Browse",
            command=self._browse_folder,
            width=100,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.browse_button.pack(side="right")
        
        # File count info
        self.file_info_label = ctk.CTkLabel(
            folder_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.file_info_label.pack(pady=(0, 10), padx=15)
        
        # Action Buttons Section
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10, padx=20)
        
        # Row 1: Main actions
        row1 = ctk.CTkFrame(button_frame, fg_color="transparent")
        row1.pack(pady=5)
        
        self.organize_button = ctk.CTkButton(
            row1,
            text="✨ Organize Files",
            command=self._organize_files,
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        self.organize_button.pack(side="left", padx=5)
        
        self.organize_clean_button = ctk.CTkButton(
            row1,
            text="✨🧹 Organize + Clean",
            command=self._organize_with_clean,
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0B7A7A",
            hover_color="#085A5A"
        )
        self.organize_clean_button.pack(side="left", padx=5)
        
        self.undo_button = ctk.CTkButton(
            row1,
            text="↶ Undo",
            command=self._undo_last,
            width=120,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#8B4513",
            hover_color="#6B3410"
        )
        self.undo_button.pack(side="left", padx=5)
        
        # Row 2: Additional actions
        row2 = ctk.CTkFrame(button_frame, fg_color="transparent")
        row2.pack(pady=5)
        
        self.quick_clean_button = ctk.CTkButton(
            row2,
            text="🧹 Quick Clean",
            command=self._quick_clean,
            width=140,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#D97706",
            hover_color="#B45309"
        )
        self.quick_clean_button.pack(side="left", padx=5)
        
        self.preview_clean_button = ctk.CTkButton(
            row2,
            text="👁️ Preview Clean",
            command=self._preview_clean,
            width=140,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6B7280",
            hover_color="#4B5563"
        )
        self.preview_clean_button.pack(side="left", padx=5)
        
        self.reload_button = ctk.CTkButton(
            row2,
            text="🔄 Reload Config",
            command=self._reload_config,
            width=140,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#4A5568",
            hover_color="#2D3748"
        )
        self.reload_button.pack(side="left", padx=5)
        
        self.summary_button = ctk.CTkButton(
            row2,
            text="📊 Export Summary",
            command=self._export_summary,
            width=140,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#7C3AED",
            hover_color="#5B21B6"
        )
        self.summary_button.pack(side="left", padx=5)
        
        # Progress Section
        progress_frame = ctk.CTkFrame(self)
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        progress_label = ctk.CTkLabel(
            progress_frame,
            text="Progress:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        progress_label.pack(pady=(10, 5), padx=15, anchor="w")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=840)
        self.progress_bar.pack(pady=(0, 10), padx=15)
        self.progress_bar.set(0)
        
        self.progress_text = ctk.CTkLabel(
            progress_frame,
            text="Ready to organize",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.progress_text.pack(pady=(0, 10), padx=15)
        
        # Log/Summary Section
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        log_label = ctk.CTkLabel(
            log_frame,
            text="Activity Log:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        log_label.pack(pady=(10, 5), padx=15, anchor="w")
        
        self.log_textbox = ctk.CTkTextbox(
            log_frame,
            width=840,
            height=150,
            font=ctk.CTkFont(size=11)
        )
        self.log_textbox.pack(pady=(0, 15), padx=15, fill="both", expand=True)
        self.log_textbox.insert("1.0", "⚡ Welcome to AA Smart Organizer!\n")
        self.log_textbox.insert("end", "✨ New: PDF Export, Safety Confirmation Dialogs, Enhanced UI\n")
        self.log_textbox.insert("end", "🚀 Select a folder and choose an action to begin.\n")
        self.log_textbox.configure(state="disabled")
        
        # Footer
        footer_label = ctk.CTkLabel(
            self,
            text="AA's Computer and Remote Services | Automate Smarter",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color=FuturisticTheme.TEXT_SECONDARY
        )
        footer_label.pack(pady=(0, 10))
    
    def _browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(title="Select Folder to Organize")
        
        if folder:
            self.selected_folder = folder
            self.folder_path_var.set(folder)
            
            # Get file count info
            total, organizable = self.organizer.get_organizable_count(folder)
            self.file_info_label.configure(
                text=f"📊 {total} files found | {organizable} can be organized"
            )
            
            self._log_message(f"Selected folder: {folder}")
            self._log_message(f"Found {organizable} files that can be organized")
    
    def _organize_files(self):
        """Start the file organization process"""
        self._start_organization(quick_clean=False)
    
    def _organize_with_clean(self):
        """Start organization with quick clean first"""
        self._start_organization(quick_clean=True)
    
    def _start_organization(self, quick_clean=False):
        """Start the file organization process"""
        if not self.selected_folder:
            self._log_message("⚠️ Please select a folder first!", "error")
            messagebox.showwarning("No Folder", "Please select a folder first!")
            return
        
        if self.is_organizing:
            self._log_message("⚠️ Organization already in progress!", "warning")
            return
        
        # Clear activity log session
        if self.activity_log:
            self.activity_log.clear_session()
        
        # Start summary tracking
        if self.summary:
            self.summary.start_operation()
        
        # Disable buttons during organization
        self._set_buttons_state("disabled")
        
        # Reset progress
        self.progress_bar.set(0)
        self.progress_text.configure(text="Starting organization...")
        
        self._log_message("\n" + "="*50)
        self._log_message("🚀 Starting file organization...")
        
        # Run organization in a separate thread
        self.is_organizing = True
        thread = threading.Thread(
            target=self._organize_thread,
            args=(quick_clean,),
            daemon=True
        )
        thread.start()
    
    def _organize_thread(self, quick_clean=False):
        """Thread function for organizing files"""
        try:
            folder = Path(self.selected_folder)
            
            # Quick clean first if requested
            if quick_clean and self.maintenance:
                self.after(0, lambda: self._log_message("\n🧹 Running Quick Clean first..."))
                stats = self.maintenance.quick_clean(
                    folder,
                    recursive=False,
                    preview_only=False,
                    clear_recycle_bin=True  # Enable Recycle Bin clearing
                )
                self.after(0, lambda: self._log_message(
                    f"✅ Cleaned {stats['junk_files_deleted']} junk files, "
                    f"freed {stats['space_freed_formatted']}\n"
                ))
            
            # Organize with progress callback
            stats = self.organizer.organize_folder(
                self.selected_folder,
                progress_callback=self._update_progress,
                undo_manager=self.undo_manager
            )
            
            # Save undo session
            self.undo_manager.save_session()
            
            # Save activity log
            if self.activity_log:
                # Log all moves
                for category, count in stats.items():
                    self.activity_log.log_action(
                        "ORGANIZE",
                        f"Organized {count} files to {category}",
                        {"category": category, "count": count}
                    )
                self.activity_log.save_undo_data()
            
            # Update UI with results
            self.after(0, self._organization_complete, stats)
            
        except Exception as e:
            self.after(0, self._organization_error, str(e))
    
    def _update_progress(self, current, total, filename):
        """Update progress bar and text"""
        progress = current / total
        
        def update_ui():
            self.progress_bar.set(progress)
            self.progress_text.configure(
                text=f"Processing: {filename} ({current}/{total})"
            )
        
        self.after(0, update_ui)
    
    def _organization_complete(self, stats):
        """Handle successful organization completion"""
        self.is_organizing = False
        self.progress_bar.set(1.0)
        self.progress_text.configure(text="✅ Organization complete!")
        
        # Generate summary
        if self.summary:
            self.summary.end_operation()
            total_moved = sum(stats.values())
            
            # Calculate total size (approximate)
            total_size = 0
            for category, count in stats.items():
                total_size += count * 1024000  # Approximate 1MB per file
            
            summary_data = self.summary.generate_summary(
                total_files=total_moved,
                files_organized=total_moved,
                files_skipped=0,
                files_failed=0,
                total_size=total_size,
                categories=stats
            )
        
        # Log summary
        self._log_message("\n✅ Organization completed successfully!")
        self._log_message("\n📊 Summary:")
        
        total_moved = 0
        for category, count in stats.items():
            self._log_message(f"   • {category}: {count} files")
            total_moved += count
        
        if total_moved == 0:
            self._log_message("   No files were moved (all files already organized or no matching files)")
        else:
            self._log_message(f"\n🎉 Total files organized: {total_moved}")
        
        self._log_message("="*50 + "\n")
        
        # Re-enable buttons
        self._set_buttons_state("normal")
        
        # Update file count
        total, organizable = self.organizer.get_organizable_count(self.selected_folder)
        self.file_info_label.configure(
            text=f"📊 {total} files found | {organizable} can be organized"
        )
    
    def _organization_error(self, error_message):
        """Handle organization error"""
        self.is_organizing = False
        self.progress_bar.set(0)
        self.progress_text.configure(text="❌ Organization failed")
        
        self._log_message(f"\n❌ Error: {error_message}", "error")
        self._log_message("="*50 + "\n")
        
        # Re-enable buttons
        self._set_buttons_state("normal")
        
        messagebox.showerror("Error", f"Organization failed: {error_message}")
    
    def _quick_clean(self):
        """Run quick clean on selected folder"""
        self._run_clean(preview=False)
    
    def _preview_clean(self):
        """Preview what will be cleaned"""
        self._run_clean(preview=True)
    
    def _run_clean(self, preview=False):
        """Run quick clean operation with confirmation dialog"""
        if not self.selected_folder:
            self._log_message("⚠️ Please select a folder first!")
            messagebox.showwarning("No Folder", "Please select a folder first!")
            return
        
        if self.is_organizing:
            self._log_message("⚠️ Cannot clean while organizing!")
            return
        
        # Show confirmation dialog (unless preview mode)
        if not preview:
            if not show_clean_confirmation_dialog(self):
                self._log_message("🚫 Quick Clean cancelled by user")
                return
        
        self._set_buttons_state("disabled")
        self.progress_text.configure(text="🧹 Scanning for junk files...")
        
        # Run in thread
        thread = threading.Thread(
            target=self._clean_thread,
            args=(preview,),
            daemon=True
        )
        thread.start()
    
    def _clean_thread(self, preview=False):
        """Thread function for cleaning"""
        try:
            folder = Path(self.selected_folder)
            
            stats = self.maintenance.quick_clean(
                folder,
                recursive=False,
                preview_only=preview,
                clear_recycle_bin=True  # Enable Recycle Bin clearing
            )
            
            self.after(0, self._clean_complete, stats, preview)
            
        except Exception as e:
            self.after(0, self._clean_error, str(e))
    
    def _clean_complete(self, stats, preview):
        """Handle clean completion"""
        self.progress_text.configure(text="✅ Clean complete!")
        
        if preview:
            self._log_message(f"\n👁️ Preview: Would clean {stats['junk_files_found']} files")
            self._log_message(f"   Would free: {stats['space_freed_formatted']}")
        else:
            self._log_message(f"\n✅ Cleaned {stats['junk_files_deleted']} files")
            self._log_message(f"   Freed: {stats['space_freed_formatted']}")
        
        self._set_buttons_state("normal")
    
    def _clean_error(self, error_message):
        """Handle clean error"""
        self.progress_text.configure(text="❌ Clean failed")
        self._log_message(f"\n❌ Clean error: {error_message}")
        self._set_buttons_state("normal")
        messagebox.showerror("Error", f"Clean failed: {error_message}")
    
    def _undo_last(self):
        """Undo the last organization"""
        if self.is_organizing:
            self._log_message("⚠️ Cannot undo while organizing!", "warning")
            return
        
        self._log_message("\n" + "="*50)
        self._log_message("↶ Attempting to undo last organization...")
        
        # Disable button during undo
        self.undo_button.configure(state="disabled")
        
        # Run undo in thread
        thread = threading.Thread(target=self._undo_thread, daemon=True)
        thread.start()
    
    def _undo_thread(self):
        """Thread function for undo operation"""
        try:
            success, message, count = self.undo_manager.undo_last_session()
            self.after(0, self._undo_complete, success, message, count)
        except Exception as e:
            self.after(0, self._undo_complete, False, f"Error: {str(e)}", 0)
    
    def _undo_complete(self, success, message, count):
        """Handle undo completion"""
        if success:
            self._log_message(f"✅ {message}")
            self._log_message(f"🔄 Restored {count} files to original locations")
            
            # Update file count if folder is selected
            if self.selected_folder:
                total, organizable = self.organizer.get_organizable_count(self.selected_folder)
                self.file_info_label.configure(
                    text=f"📊 {total} files found | {organizable} can be organized"
                )
        else:
            self._log_message(f"⚠️ {message}", "warning")
        
        self._log_message("="*50 + "\n")
        
        # Re-enable button
        self.undo_button.configure(state="normal")
    
    def _reload_config(self):
        """Reload configuration from config.json"""
        if self.is_organizing:
            self._log_message("⚠️ Cannot reload config while organizing!", "warning")
            return
        
        self._log_message("\n" + "="*50)
        self._log_message("🔄 Reloading configuration...")
        
        # Disable button during reload
        self.reload_button.configure(state="disabled")
        
        # Reload config
        success, message, count = self.organizer.reload_config()
        
        if success:
            self._log_message(f"✅ {message}")
            
            # Update file count if folder is selected
            if self.selected_folder:
                total, organizable = self.organizer.get_organizable_count(self.selected_folder)
                self.file_info_label.configure(
                    text=f"📊 {total} files found | {organizable} can be organized"
                )
                self._log_message(f"Updated: {organizable} files can now be organized")
        else:
            self._log_message(f"❌ {message}", "error")
        
        self._log_message("="*50 + "\n")
        
        # Re-enable button
        self.reload_button.configure(state="normal")
    
    def _export_summary(self):
        """Export summary report with PDF option"""
        if not self.summary or not self.summary.operation_data:
            messagebox.showinfo("No Data", "No summary data available. Organize files first!")
            return
        
        # Ask for save location with PDF option
        filename = filedialog.asksaveasfilename(
            title="Export Summary - PDF, HTML, or Text",
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("HTML files", "*.html"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            # Export based on file extension
            if filename.endswith('.pdf'):
                success = self.summary.export_to_pdf(Path(filename))
            elif filename.endswith('.html'):
                success = self.summary.export_to_html(Path(filename))
            else:
                success = self.summary.export_to_text(Path(filename))
            
            if success:
                self._log_message(f"✅ Summary exported to: {filename}")
                messagebox.showinfo("Success", f"Summary exported to:\n{filename}")
            else:
                self._log_message(f"❌ Failed to export summary")
                messagebox.showerror("Error", "Failed to export summary")
    
    def _set_buttons_state(self, state):
        """Enable or disable all buttons"""
        self.organize_button.configure(state=state)
        self.organize_clean_button.configure(state=state)
        self.undo_button.configure(state=state)
        self.quick_clean_button.configure(state=state)
        self.preview_clean_button.configure(state=state)
        self.reload_button.configure(state=state)
        self.browse_button.configure(state=state)
    
    def _log_message(self, message, level="info"):
        """Add a message to the log textbox"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")


def main():
    """Main entry point"""
    app = AASmartOrganizerV3()
    app.mainloop()


if __name__ == "__main__":
    main()
