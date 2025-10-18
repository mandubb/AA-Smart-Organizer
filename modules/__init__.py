"""
AA Smart Organizer - Modules Package
Modular components for file organization and maintenance
"""

from .utils import (
    format_file_size,
    get_file_size,
    ensure_directory,
    load_json,
    save_json,
    get_timestamp,
    get_date_string,
    is_junk_file,
    calculate_duration
)

from .activity_log import ActivityLog
from .maintenance import MaintenanceManager
from .profiles import ProfileManager
from .summary import SummaryGenerator
from .scheduler import TaskScheduler

__all__ = [
    'format_file_size',
    'get_file_size',
    'ensure_directory',
    'load_json',
    'save_json',
    'get_timestamp',
    'get_date_string',
    'is_junk_file',
    'calculate_duration',
    'ActivityLog',
    'MaintenanceManager',
    'ProfileManager',
    'SummaryGenerator',
    'TaskScheduler'
]

__version__ = '2.0.0'
__author__ = "AA's Computer and Remote Services"
