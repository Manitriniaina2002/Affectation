from typing import Dict, List, Optional, Tuple, Any
from .base_model import BaseModel

class Location(BaseModel):
    """Model representing a location in the system."""
    
    TABLE_NAME = 'LIEU'
    PRIMARY_KEY = 'idlieu'
    FIELDS = {
        'idlieu': 'TEXT',
        'design': 'TEXT',
        'province': 'TEXT'
    }
    
    def __init__(self, idlieu: str = None, design: str = None, province: str = None):
        """Initialize a Location instance.
        
        Args:
            idlieu: Unique identifier for the location
            design: Designation/name of the location
            province: Province where the location is situated
        """
        super().__init__()
        self.idlieu = idlieu
        self.design = design
        self.province = province
    
    def validate(self) -> Tuple[bool, str]:
        """Validate the location data before saving.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not self.idlieu or not self.idlieu.strip():
            return False, "Location ID is required."
        if not self.design or not self.design.strip():
            return False, "Location designation is required."
        if not self.province or not self.province.strip():
            return False, "Province is required."
        return True, ""
    
    # Additional business logic methods can be added here
    
    @classmethod
    def get_by_province(cls, db: 'Database', province: str) -> List['Location']:
        """Get all locations in a specific province.
        
        Args:
            db: Database connection
            province: Province name to filter by
            
        Returns:
            List[Location]: List of locations in the specified province
        """
        cursor = db.conn.cursor()
        cursor.execute(f"""
            SELECT * FROM {cls.TABLE_NAME}
            WHERE province = ?
            ORDER BY design
        """, (province,))
        
        return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_provinces(cls, db: 'Database') -> List[str]:
        """Get a list of all unique provinces.
        
        Args:
            db: Database connection
            
        Returns:
            List[str]: Sorted list of unique province names
        """
        cursor = db.conn.cursor()
        cursor.execute(f"""
            SELECT DISTINCT province 
            FROM {cls.TABLE_NAME}
            ORDER BY province
        """)
        
        return [row[0] for row in cursor.fetchall() if row[0]]
