"""
Base controller class for the Employee Assignment Management System.
This module provides a base class for all controllers in the application.
"""
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union
from abc import ABC, abstractmethod

from ..models.database import Database
from ..models.location import Location
from ..models.employee import Employee
from ..models.assignment import Assignment

T = TypeVar('T')

class BaseController(ABC):
    """Base controller class that provides common functionality for all controllers."""
    
    def __init__(self, db: Database):
        """Initialize the base controller.
        
        Args:
            db: Database connection
        """
        self.db = db
        
    @abstractmethod
    def get_all(self, **kwargs) -> List[Any]:
        """Get all items.
        
        Args:
            **kwargs: Additional filters/parameters
            
        Returns:
            List of items
        """
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: Any) -> Optional[Any]:
        """Get an item by ID.
        
        Args:
            item_id: Item ID
            
        Returns:
            The item, or None if not found
        """
        pass
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Create a new item.
        
        Args:
            data: Item data
            
        Returns:
            Tuple of (success, message)
        """
        pass
    
    @abstractmethod
    def update(self, item_id: Any, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update an existing item.
        
        Args:
            item_id: Item ID
            data: Updated item data
            
        Returns:
            Tuple of (success, message)
        """
        pass
    
    @abstractmethod
    def delete(self, item_id: Any) -> Tuple[bool, str]:
        """Delete an item.
        
        Args:
            item_id: Item ID
            
        Returns:
            Tuple of (success, message)
        """
        pass
    
    def _validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, str]:
        """Validate that all required fields are present in the data.
        
        Args:
            data: Data to validate
            required_fields: List of required field names
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        return True, ""
    
    def _get_next_id(self, prefix: str, existing_ids: List[str]) -> str:
        """Generate the next available ID with the given prefix.
        
        Args:
            prefix: Prefix for the ID (e.g., 'EMP' for employee IDs)
            existing_ids: List of existing IDs to check against
            
        Returns:
            str: The next available ID
        """
        if not existing_ids:
            return f"{prefix}001"
            
        # Extract numeric parts and find the maximum
        numbers = []
        for id_str in existing_ids:
            if id_str and id_str.startswith(prefix):
                try:
                    num = int(id_str[len(prefix):])
                    numbers.append(num)
                except (ValueError, IndexError):
                    continue
                    
        if not numbers:
            return f"{prefix}001"
            
        next_num = max(numbers) + 1
        return f"{prefix}{next_num:03d}"
