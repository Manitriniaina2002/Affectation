""
Location controller for the Employee Assignment Management System.

This module handles all business logic related to locations.
"""
from typing import Any, Dict, List, Optional, Tuple

from ..models.location import Location
from .base_controller import BaseController

class LocationController(BaseController):
    """Controller for location-related operations."""
    
    def get_all(self, **kwargs) -> List[Location]:
        """Get all locations.
        
        Args:
            **kwargs: Additional filters/parameters
                - province: Filter by province
                
        Returns:
            List of Location objects
        """
        province = kwargs.get('province')
        
        if province:
            return Location.get_by_province(self.db, province)
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM LIEU ORDER BY province, design")
        return [Location.from_row(row) for row in cursor.fetchall()]
    
    def get_by_id(self, location_id: str) -> Optional[Location]:
        """Get a location by ID.
        
        Args:
            location_id: Location ID
            
        Returns:
            Location object, or None if not found
        """
        return Location.get(self.db, location_id)
    
    def create(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Create a new location.
        
        Args:
            data: Location data with keys:
                - idlieu: Location ID
                - design: Location name
                - province: Province name
                
        Returns:
            Tuple of (success, message)
        """
        # Validate required fields
        required_fields = ['idlieu', 'design', 'province']
        is_valid, error_msg = self._validate_required_fields(data, required_fields)
        if not is_valid:
            return False, error_msg
        
        # Create location object
        location = Location(
            idlieu=data['idlieu'].strip(),
            design=data['design'].strip(),
            province=data['province'].strip()
        )
        
        # Validate location
        is_valid, error_msg = location.validate()
        if not is_valid:
            return False, error_msg
        
        # Check if location ID already exists
        existing = self.get_by_id(location.idlieu)
        if existing:
            return False, f"Location with ID '{location.idlieu}' already exists."
        
        # Save to database
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "INSERT INTO LIEU (idlieu, design, province) VALUES (?, ?, ?)",
                (location.idlieu, location.design, location.province)
            )
            self.db.conn.commit()
            return True, "Location created successfully!"
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error creating location: {str(e)}"
    
    def update(self, location_id: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update an existing location.
        
        Args:
            location_id: ID of the location to update
            data: Updated location data with keys:
                - design: New location name
                - province: New province name
                
        Returns:
            Tuple of (success, message)
        """
        # Get existing location
        location = self.get_by_id(location_id)
        if not location:
            return False, "Location not found."
        
        # Update fields
        if 'design' in data:
            location.design = data['design'].strip()
        if 'province' in data:
            location.province = data['province'].strip()
        
        # Validate location
        is_valid, error_msg = location.validate()
        if not is_valid:
            return False, error_msg
        
        # Save to database
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "UPDATE LIEU SET design = ?, province = ? WHERE idlieu = ?",
                (location.design, location.province, location_id)
            )
            
            if cursor.rowcount == 0:
                return False, "Location not found."
                
            self.db.conn.commit()
            return True, "Location updated successfully!"
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error updating location: {str(e)}"
    
    def delete(self, location_id: str) -> Tuple[bool, str]:
        """Delete a location.
        
        Args:
            location_id: ID of the location to delete
            
        Returns:
            Tuple of (success, message)
        """
        # Check if location exists
        location = self.get_by_id(location_id)
        if not location:
            return False, "Location not found."
        
        # Check if location is referenced by employees
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM EMPLOYE WHERE idlieu = ?", (location_id,))
        if cursor.fetchone()[0] > 0:
            return False, "Cannot delete location: Employees are assigned to this location."
        
        # Check if location is referenced in assignments
        cursor.execute("""
            SELECT COUNT(*) 
            FROM AFFECTER 
            WHERE AncienLieu = ? OR NouveauLieu = ?
        """, (location_id, location_id))
        
        if cursor.fetchone()[0] > 0:
            return False, "Cannot delete location: Location is referenced in assignment history."
        
        # Delete location
        try:
            cursor.execute("DELETE FROM LIEU WHERE idlieu = ?", (location_id,))
            
            if cursor.rowcount == 0:
                return False, "Location not found."
                
            self.db.conn.commit()
            return True, "Location deleted successfully!"
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error deleting location: {str(e)}"
    
    def get_provinces(self) -> List[str]:
        """Get a list of all unique provinces.
        
        Returns:
            List of province names
        """
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT province 
            FROM LIEU
            ORDER BY province
        """)
        
        return [row[0] for row in cursor.fetchall() if row[0]]
    
    def get_locations_by_province(self, province: str) -> List[Location]:
        """Get all locations in a specific province.
        
        Args:
            province: Province name
            
        Returns:
            List of Location objects in the specified province
        """
        return Location.get_by_province(self.db, province)
