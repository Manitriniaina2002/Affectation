"""
Models package for the Employee Assignment Management System.

This package contains the data models and database operations for the application.
"""

from .database import Database
from .location import Location
from .employee import Employee
from .assignment import Assignment

__all__ = ['Database', 'Location', 'Employee', 'Assignment']
