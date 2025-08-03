""
Helper functions and utilities for the Employee Assignment Management System.
"""
import os
import csv
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Tuple, Union

def format_date(date_str: Optional[str], fmt: str = '%Y-%m-%d') -> Optional[str]:
    """Format a date string from one format to another.
    
    Args:
        date_str: Date string to format
        fmt: Target format (default: '%Y-%m-%d')
        
    Returns:
        Formatted date string, or None if input is None or empty
    """
    if not date_str:
        return None
        
    try:
        # Try parsing with date
        date_obj = datetime.strptime(str(date_str), '%Y-%m-%d').date()
        return date_obj.strftime(fmt)
    except (ValueError, TypeError):
        return str(date_str)

def parse_date(date_str: str, fmt: str = '%Y-%m-%d') -> Optional[date]:
    """Parse a date string into a date object.
    
    Args:
        date_str: Date string to parse
        fmt: Expected format (default: '%Y-%m-%d')
        
    Returns:
        Date object, or None if parsing fails
    """
    if not date_str:
        return None
        
    try:
        return datetime.strptime(str(date_str), fmt).date()
    except (ValueError, TypeError):
        return None

def validate_email(email: str) -> bool:
    """Validate an email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if the email is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
        
    # Simple email validation
    return '@' in email and '.' in email.split('@')[-1]

def export_to_csv(data: List[Dict[str, Any]], filepath: str) -> Tuple[bool, str]:
    """Export data to a CSV file.
    
    Args:
        data: List of dictionaries to export
        filepath: Path to save the CSV file
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    if not data:
        return False, "No data to export"
        
    try:
        # Get fieldnames from the first dictionary
        fieldnames = list(data[0].keys())
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        return True, f"Data exported successfully to {filepath}"
    except Exception as e:
        return False, f"Error exporting to CSV: {str(e)}"

def get_next_id(prefix: str, existing_ids: List[str]) -> str:
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
        if id_str.startswith(prefix):
            try:
                num = int(id_str[len(prefix):])
                numbers.append(num)
            except (ValueError, IndexError):
                continue
                
    if not numbers:
        return f"{prefix}001"
        
    next_num = max(numbers) + 1
    return f"{prefix}{next_num:03d}"

def format_currency(amount: Union[int, float, str]) -> str:
    """Format a number as currency.
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    try:
        num = float(amount)
        return f"{num:,.2f} MGA"
    except (ValueError, TypeError):
        return str(amount)

def truncate_string(text: str, max_length: int = 50, ellipsis: str = '...') -> str:
    """Truncate a string to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of the result string
        ellipsis: String to append if text is truncated
        
    Returns:
        Truncated string with ellipsis if needed
    """
    if not text or len(text) <= max_length:
        return text
        
    return text[:max_length - len(ellipsis)] + ellipsis

def format_full_name(civilite: str, nom: str, prenom: str) -> str:
    """Format a full name with title.
    
    Args:
        civilite: Title (Mr, Mme, Mlle)
        nom: Last name
        prenom: First name
        
    Returns:
        Formatted full name
    """
    if not nom and not prenom:
        return ""
        
    title = {
        'Mr': 'M.',
        'Mme': 'Mme',
        'Mlle': 'Mlle'
    }.get(civilite, '')
    
    name_parts = [part for part in [title, prenom, nom.upper()] if part]
    return ' '.join(name_parts)
