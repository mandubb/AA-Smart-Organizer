"""
AA Smart Organizer - Main Application
A modern desktop app for organizing messy folders automatically
"""

import os
import sys
import threading
from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk

# Import our modules
from organizer import FileOrganizer
from undo_manager import UndoManager


class AASmartOrganizer(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("AA Smart Organizer")
        self.geometry("700x550")
        self.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize components
        self.organizer = FileOrganizer()
        self.undo_manager = UndoManager()
        self.selected_folder = None
        self.is_organizing = False
        
        # Create UI
        self._create_ui()
    
    def _create_ui(self):
        """Build the user interface"""
        
        # Title Section
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=(20, 10), padx=20, fill="x")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🗂️ AA Smart Organizer",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Organize your messy folders automatically",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Folder Selection Section
        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(pady=20, padx=20, fill="x")
        
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
        
        self.organize_button = ctk.CTkButton(
            button_frame,
            text="✨ Organize Files",
            command=self._organize_files,
            width=200,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        self.organize_button.pack(side="left", padx=10)
        
        self.undo_button = ctk.CTkButton(
            button_frame,
            text="↶ Undo Last Action",
            command=self._undo_last,
            width=200,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#8B4513",
            hover_color="#6B3410"
        )
        self.undo_button.pack(side="right", padx=10)
        
        # Progress Section
        progress_frame = ctk.CTkFrame(self)
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        progress_label = ctk.CTkLabel(
            progress_frame,
            text="Progress:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        progress_label.pack(pady=(10, 5), padx=15, anchor="w")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=640)
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
            width=640,
            height=120,
            font=ctk.CTkFont(size=11)
        )
        self.log_textbox.pack(pady=(0, 15), padx=15, fill="both", expand=True)
        self.log_textbox.insert("1.0", "Welcome to AA Smart Organizer!\nSelect a folder and click 'Organize Files' to begin.\n")
        self.log_textbox.configure(state="disabled")
        
        # Footer
        footer_label = ctk.CTkLabel(
            self,
            text="AA's Computer and Remote Services",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color="gray"
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
        if not self.selected_folder:
            self._log_message("⚠️ Please select a folder first!", "error")
            return
        
        if self.is_organizing:
            self._log_message("⚠️ Organization already in progress!", "warning")
            return
        
        # Clear undo manager's current session
        self.undo_manager.clear_session()
        
        # Disable buttons during organization
        self.organize_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        
        # Reset progress
        self.progress_bar.set(0)
        self.progress_text.configure(text="Starting organization...")
        
        self._log_message("\n" + "="*50)
        self._log_message("🚀 Starting file organization...")
        
        # Run organization in a separate thread
        self.is_organizing = True
        thread = threading.Thread(target=self._organize_thread, daemon=True)
        thread.start()
    
    def _organize_thread(self):
        """Thread function for organizing files"""
        try:
            # Organize with progress callback
            stats = self.organizer.organize_folder(
                self.selected_folder,
                progress_callback=self._update_progress,
                undo_manager=self.undo_manager
            )
            
            # Save undo session
            self.undo_manager.save_session()
            
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
        self.organize_button.configure(state="normal")
        self.browse_button.configure(state="normal")
        
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
        self.organize_button.configure(state="normal")
        self.browse_button.configure(state="normal")
    
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
    
    def _log_message(self, message, level="info"):
        """Add a message to the log textbox"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", message + "\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")


def main():
    """Main entry point"""
    app = AASmartOrganizer()
    app.mainloop()


if __name__ == "__main__":
    main()
