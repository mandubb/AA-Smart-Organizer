"""
Futuristic GUI Module - Part 1: Core Interface
Modern, dark-themed interface with glowing accents
"""

import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional, Callable
from datetime import datetime

class FuturisticTheme:
    """Color scheme for futuristic interface"""
    BG_DARK = '#0A0E27'
    BG_MEDIUM = '#151B3D'
    BG_LIGHT = '#1E2749'
    ACCENT_CYAN = '#00D9FF'
    ACCENT_BLUE = '#0066FF'
    ACCENT_PURPLE = '#9D00FF'
    ACCENT_GREEN = '#00FF88'
    TEXT_PRIMARY = '#FFFFFF'
    TEXT_SECONDARY = '#8B9DC3'
    SUCCESS = '#10B981'
    WARNING = '#F59E0B'
    ERROR = '#EF4444'


def show_clean_confirmation_dialog(parent) -> bool:
    """
    Show confirmation dialog for Quick Clean
    
    Args:
        parent: Parent window
        
    Returns:
        bool: True if user confirmed, False if cancelled
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("⚠️ Confirm Quick Clean")
    dialog.geometry("600x450")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()
    
    # Center dialog
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
    y = (dialog.winfo_screenheight() // 2) - (450 // 2)
    dialog.geometry(f"+{x}+{y}")
    
    result = [False]
    
    # Content
    content_frame = ctk.CTkFrame(dialog, fg_color=FuturisticTheme.BG_DARK)
    content_frame.pack(fill="both", expand=True)
    
    # Warning icon
    icon_label = ctk.CTkLabel(
        content_frame,
        text="⚠️",
        font=ctk.CTkFont(size=60),
        text_color=FuturisticTheme.WARNING
    )
    icon_label.pack(pady=(30, 20))
    
    # Title
    title_label = ctk.CTkLabel(
        content_frame,
        text="CONFIRM QUICK CLEAN",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color=FuturisticTheme.TEXT_PRIMARY
    )
    title_label.pack(pady=(0, 20))
    
    # Warning text
    warning_frame = ctk.CTkFrame(
        content_frame,
        fg_color=FuturisticTheme.BG_MEDIUM,
        corner_radius=10
    )
    warning_frame.pack(fill="x", padx=30, pady=(0, 20))
    
    warning_text = ctk.CTkLabel(
        warning_frame,
        text="This operation will PERMANENTLY DELETE:\n\n"
             "• Temporary files (.tmp, .temp, .log, .cache)\n"
             "• System junk (Thumbs.db, desktop.ini, .DS_Store)\n"
             "• Office temp files (~$)\n"
             "• Empty folders\n"
             "• Recycle Bin contents (Windows)\n\n"
             "⚠️ This action CANNOT be undone!\n\n"
             "Do you want to proceed?",
        font=ctk.CTkFont(size=12),
        text_color=FuturisticTheme.TEXT_PRIMARY,
        justify="left"
    )
    warning_text.pack(padx=20, pady=20)
    
    # Buttons
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    def on_confirm():
        result[0] = True
        dialog.destroy()
    
    def on_cancel():
        result[0] = False
        dialog.destroy()
    
    cancel_btn = ctk.CTkButton(
        button_frame,
        text="❌ CANCEL",
        command=on_cancel,
        width=250,
        height=50,
        corner_radius=10,
        fg_color=FuturisticTheme.BG_LIGHT,
        hover_color=FuturisticTheme.BG_MEDIUM,
        text_color=FuturisticTheme.TEXT_PRIMARY,
        font=ctk.CTkFont(size=14, weight="bold")
    )
    cancel_btn.pack(side="left", padx=5)
    
    confirm_btn = ctk.CTkButton(
        button_frame,
        text="✅ YES, CLEAN NOW",
        command=on_confirm,
        width=250,
        height=50,
        corner_radius=10,
        fg_color=FuturisticTheme.ACCENT_GREEN,
        hover_color=FuturisticTheme.SUCCESS,
        text_color=FuturisticTheme.BG_DARK,
        font=ctk.CTkFont(size=14, weight="bold")
    )
    confirm_btn.pack(side="right", padx=5)
    
    # Wait for dialog to close
    parent.wait_window(dialog)
    
    return result[0]
