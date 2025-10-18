"""
Scheduler Module
Handles automatic scheduling of organization tasks
"""

import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional, Callable, Dict
from datetime import datetime
from .utils import get_timestamp, save_json, load_json


class TaskScheduler:
    """Manages scheduled tasks and automated runs"""
    
    def __init__(self, config_path: Path):
        """
        Initialize task scheduler
        
        Args:
            config_path: Path to scheduler configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.is_running = False
        self.scheduled_jobs = []
    
    def _load_config(self) -> Dict:
        """Load scheduler configuration"""
        default_config = {
            "enabled": False,
            "schedules": [],
            "email_notifications": {
                "enabled": False,
                "smtp_server": "",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipient_email": ""
            }
        }
        return load_json(self.config_path, default_config)
    
    def save_config(self) -> bool:
        """Save scheduler configuration"""
        return save_json(self.config_path, self.config)
    
    def add_schedule(
        self,
        schedule_type: str,
        time_str: str,
        folder_path: str,
        profile: str = "default",
        quick_clean: bool = False
    ) -> bool:
        """
        Add a new schedule
        
        Args:
            schedule_type: Type of schedule (daily, weekly, monthly)
            time_str: Time string (e.g., "14:30" or "Monday 10:00")
            folder_path: Path to folder to organize
            profile: Profile to use
            quick_clean: Whether to run quick clean
            
        Returns:
            bool: True if successful
        """
        schedule_entry = {
            "id": f"schedule_{len(self.config['schedules']) + 1}",
            "type": schedule_type,
            "time": time_str,
            "folder_path": folder_path,
            "profile": profile,
            "quick_clean": quick_clean,
            "enabled": True,
            "created": get_timestamp(),
            "last_run": None
        }
        
        self.config['schedules'].append(schedule_entry)
        return self.save_config()
    
    def remove_schedule(self, schedule_id: str) -> bool:
        """
        Remove a schedule
        
        Args:
            schedule_id: ID of schedule to remove
            
        Returns:
            bool: True if successful
        """
        self.config['schedules'] = [
            s for s in self.config['schedules']
            if s['id'] != schedule_id
        ]
        return self.save_config()
    
    def list_schedules(self) -> list:
        """
        List all schedules
        
        Returns:
            list: List of schedule entries
        """
        return self.config['schedules']
    
    def setup_schedules(self, task_callback: Callable) -> None:
        """
        Setup all schedules with the schedule library
        
        Args:
            task_callback: Function to call when schedule triggers
        """
        # Clear existing jobs
        schedule.clear()
        self.scheduled_jobs = []
        
        for sched in self.config['schedules']:
            if not sched.get('enabled', True):
                continue
            
            schedule_type = sched['type']
            time_str = sched['time']
            
            # Create job based on schedule type
            if schedule_type == 'daily':
                job = schedule.every().day.at(time_str).do(
                    task_callback,
                    folder_path=sched['folder_path'],
                    profile=sched['profile'],
                    quick_clean=sched.get('quick_clean', False),
                    schedule_id=sched['id']
                )
                self.scheduled_jobs.append(job)
            
            elif schedule_type == 'weekly':
                # Parse day and time (e.g., "Monday 10:00")
                parts = time_str.split()
                if len(parts) == 2:
                    day, time = parts
                    job = getattr(schedule.every(), day.lower()).at(time).do(
                        task_callback,
                        folder_path=sched['folder_path'],
                        profile=sched['profile'],
                        quick_clean=sched.get('quick_clean', False),
                        schedule_id=sched['id']
                    )
                    self.scheduled_jobs.append(job)
            
            elif schedule_type == 'monthly':
                # Run on first day of month at specified time
                job = schedule.every().day.at(time_str).do(
                    self._check_monthly_run,
                    task_callback=task_callback,
                    folder_path=sched['folder_path'],
                    profile=sched['profile'],
                    quick_clean=sched.get('quick_clean', False),
                    schedule_id=sched['id']
                )
                self.scheduled_jobs.append(job)
        
        print(f"✅ Setup {len(self.scheduled_jobs)} scheduled tasks")
    
    def _check_monthly_run(
        self,
        task_callback: Callable,
        folder_path: str,
        profile: str,
        quick_clean: bool,
        schedule_id: str
    ) -> None:
        """Check if it's the first day of the month and run task"""
        if datetime.now().day == 1:
            task_callback(folder_path, profile, quick_clean, schedule_id)
    
    def start(self, task_callback: Callable) -> None:
        """
        Start the scheduler
        
        Args:
            task_callback: Function to call when schedule triggers
        """
        if not self.config.get('enabled', False):
            print("⚠️ Scheduler is disabled in configuration")
            return
        
        self.setup_schedules(task_callback)
        self.is_running = True
        
        print("🕒 Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n⏹️ Scheduler stopped")
            self.is_running = False
    
    def stop(self) -> None:
        """Stop the scheduler"""
        self.is_running = False
        schedule.clear()
    
    def update_last_run(self, schedule_id: str) -> None:
        """
        Update last run timestamp for a schedule
        
        Args:
            schedule_id: ID of the schedule
        """
        for sched in self.config['schedules']:
            if sched['id'] == schedule_id:
                sched['last_run'] = get_timestamp()
                break
        self.save_config()
    
    def send_email_report(
        self,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """
        Send email report
        
        Args:
            subject: Email subject
            body: Plain text body
            html_body: Optional HTML body
            
        Returns:
            bool: True if successful
        """
        email_config = self.config.get('email_notifications', {})
        
        if not email_config.get('enabled', False):
            print("⚠️ Email notifications are disabled")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['recipient_email']
            
            # Add plain text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)
            
            print(f"✅ Email sent to {email_config['recipient_email']}")
            return True
        
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def configure_email(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str,
        recipient_email: str,
        enabled: bool = True
    ) -> bool:
        """
        Configure email notifications
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP port
            sender_email: Sender email address
            sender_password: Sender email password
            recipient_email: Recipient email address
            enabled: Whether to enable email notifications
            
        Returns:
            bool: True if successful
        """
        self.config['email_notifications'] = {
            "enabled": enabled,
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "sender_email": sender_email,
            "sender_password": sender_password,
            "recipient_email": recipient_email
        }
        return self.save_config()
    
    def get_next_run_times(self) -> Dict[str, str]:
        """
        Get next run times for all schedules
        
        Returns:
            dict: Schedule ID -> next run time
        """
        next_runs = {}
        
        for job in self.scheduled_jobs:
            # Get schedule ID from job tags or function args
            schedule_id = "unknown"
            if hasattr(job, 'job_func') and hasattr(job.job_func, 'keywords'):
                schedule_id = job.job_func.keywords.get('schedule_id', 'unknown')
            
            next_run = job.next_run
            if next_run:
                next_runs[schedule_id] = next_run.strftime("%Y-%m-%d %H:%M:%S")
        
        return next_runs
    
    def create_windows_task(
        self,
        task_name: str,
        script_path: Path,
        schedule_type: str,
        time_str: str
    ) -> bool:
        """
        Create a Windows Task Scheduler task (Windows only)
        
        Args:
            task_name: Name of the task
            script_path: Path to Python script to run
            schedule_type: Type of schedule (daily, weekly)
            time_str: Time string (e.g., "14:30")
            
        Returns:
            bool: True if successful
        """
        import os
        if os.name != 'nt':
            print("⚠️ Windows Task Scheduler only available on Windows")
            return False
        
        try:
            import subprocess
            
            # Build schtasks command
            if schedule_type == 'daily':
                cmd = [
                    'schtasks', '/create',
                    '/tn', task_name,
                    '/tr', f'python "{script_path}"',
                    '/sc', 'daily',
                    '/st', time_str,
                    '/f'  # Force create
                ]
            elif schedule_type == 'weekly':
                # Parse day and time
                parts = time_str.split()
                if len(parts) == 2:
                    day, time = parts
                    cmd = [
                        'schtasks', '/create',
                        '/tn', task_name,
                        '/tr', f'python "{script_path}"',
                        '/sc', 'weekly',
                        '/d', day.upper(),
                        '/st', time,
                        '/f'
                    ]
                else:
                    print("❌ Invalid time format for weekly schedule")
                    return False
            else:
                print(f"❌ Unsupported schedule type: {schedule_type}")
                return False
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Created Windows Task: {task_name}")
                return True
            else:
                print(f"❌ Error creating task: {result.stderr}")
                return False
        
        except Exception as e:
            print(f"❌ Error creating Windows Task: {e}")
            return False
