""
Assignment controller for the Employee Assignment Management System.

This module handles all business logic related to employee assignments.
"""
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from ..models.assignment import Assignment
from ..models.employee import Employee
from ..models.location import Location
from .base_controller import BaseController

class AssignmentController(BaseController):
    """Controller for assignment-related operations."""
    
    def get_all(self, **kwargs) -> List[Assignment]:
        """Get all assignments with employee and location details.
        
        Args:
            **kwargs: Additional filters/parameters
                - employee_id: Filter by employee ID
                - start_date: Filter assignments after this date (YYYY-MM-DD)
                - end_date: Filter assignments before this date (YYYY-MM-DD)
                - limit: Maximum number of assignments to return
                
        Returns:
            List of Assignment objects with joined data
        """
        employee_id = kwargs.get('employee_id')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        limit = kwargs.get('limit')
        
        if employee_id:
            return self.get_employee_assignments(employee_id, limit=limit)
            
        if start_date and end_date:
            return self.get_assignments_between_dates(start_date, end_date)
        
        if limit:
            return Assignment.get_recent_assignments(self.db, limit=limit)
        
        # Default: get all assignments
        return Assignment.get_all_assignments(self.db)
    
    def get_by_id(self, assignment_id: str) -> Optional[Assignment]:
        """Get an assignment by ID with all related data.
        
        Args:
            assignment_id: Assignment ID
            
        Returns:
            Assignment object with joined data, or None if not found
        """
        return Assignment.get_assignment(self.db, assignment_id)
    
    def create(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Create a new assignment.
        
        This will also update the employee's current location.
        
        Args:
            data: Assignment data with keys:
                - numAffect: Assignment ID (optional, will be generated if not provided)
                - numEmp: Employee ID
                - AncienLieu: Previous location ID
                - NouveauLieu: New location ID
                - dateAffect: Assignment date (YYYY-MM-DD)
                - datePriseService: Service start date (YYYY-MM-DD)
                
        Returns:
            Tuple of (success, message, assignment_id)
        """
        # Validate required fields
        required_fields = ['numEmp', 'AncienLieu', 'NouveauLieu', 'dateAffect', 'datePriseService']
        is_valid, error_msg = self._validate_required_fields(data, required_fields)
        if not is_valid:
            return False, error_msg, None
        
        # Generate assignment ID if not provided
        if 'numAffect' not in data or not data['numAffect']:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT numAffect FROM AFFECTER")
            existing_ids = [row[0] for row in cursor.fetchall()]
            data['numAffect'] = self._get_next_id('A', existing_ids)
        
        # Create assignment object
        assignment = Assignment(
            numAffect=data['numAffect'].strip(),
            numEmp=data['numEmp'].strip(),
            AncienLieu=data['AncienLieu'].strip(),
            NouveauLieu=data['NouveauLieu'].strip(),
            dateAffect=data['dateAffect'],
            datePriseService=data['datePriseService']
        )
        
        # Validate assignment
        is_valid, error_msg = assignment.validate()
        if not is_valid:
            return False, error_msg, None
        
        # Check if employee exists
        employee = Employee.get(self.db, assignment.numEmp)
        if not employee:
            return False, f"Employee with ID '{assignment.numEmp}' not found.", None
        
        # Check if locations exist
        old_location = Location.get(self.db, assignment.AncienLieu)
        if not old_location:
            return False, f"Location with ID '{assignment.AncienLieu}' not found.", None
            
        new_location = Location.get(self.db, assignment.NouveauLieu)
        if not new_location:
            return False, f"Location with ID '{assignment.NouveauLieu}' not found.", None
        
        # Check if employee's current location matches the old location
        if employee.idlieu != assignment.AncienLieu:
            current_location = f"{employee.lieu_design} ({employee.province})" if employee.idlieu else "unassigned"
            return False, (
                f"Employee's current location ({current_location}) "
                f"does not match the specified old location ({old_location.design})."
            ), None
        
        # Save to database
        try:
            cursor = self.db.conn.cursor()
            
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Add assignment record
            cursor.execute("""
                INSERT INTO AFFECTER (
                    numAffect, numEmp, AncienLieu, 
                    NouveauLieu, dateAffect, datePriseService
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                assignment.numAffect, assignment.numEmp, assignment.AncienLieu,
                assignment.NouveauLieu, assignment.dateAffect, assignment.datePriseService
            ))
            
            # Update employee's current location
            cursor.execute(
                "UPDATE EMPLOYE SET idlieu = ? WHERE numEmp = ?",
                (assignment.NouveauLieu, assignment.numEmp)
            )
            
            self.db.conn.commit()
            return True, "Assignment created successfully!", assignment.numAffect
            
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error creating assignment: {str(e)}", None
    
    def update(self, assignment_id: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update an existing assignment.
        
        This will also update the employee's current location if the new location changes.
        
        Args:
            assignment_id: ID of the assignment to update
            data: Updated assignment data with keys:
                - numEmp: Employee ID
                - AncienLieu: Previous location ID
                - NouveauLieu: New location ID
                - dateAffect: Assignment date (YYYY-MM-DD)
                - datePriseService: Service start date (YYYY-MM-DD)
                
        Returns:
            Tuple of (success, message)
        """
        # Get existing assignment
        assignment = self.get_by_id(assignment_id)
        if not assignment:
            return False, "Assignment not found."
        
        # Update fields
        if 'numEmp' in data:
            assignment.numEmp = data['numEmp'].strip()
        if 'AncienLieu' in data:
            assignment.AncienLieu = data['AncienLieu'].strip()
        if 'NouveauLieu' in data:
            assignment.NouveauLieu = data['NouveauLieu'].strip()
        if 'dateAffect' in data:
            assignment.dateAffect = data['dateAffect']
        if 'datePriseService' in data:
            assignment.datePriseService = data['datePriseService']
        
        # Validate assignment
        is_valid, error_msg = assignment.validate()
        if not is_valid:
            return False, error_msg
        
        # Check if employee exists
        employee = Employee.get(self.db, assignment.numEmp)
        if not employee:
            return False, f"Employee with ID '{assignment.numEmp}' not found."
        
        # Check if locations exist
        old_location = Location.get(self.db, assignment.AncienLieu)
        if not old_location:
            return False, f"Location with ID '{assignment.AncienLieu}' not found."
            
        new_location = Location.get(self.db, assignment.NouveauLieu)
        if not new_location:
            return False, f"Location with ID '{assignment.NouveauLieu}' not found."
        
        # Check if this is the most recent assignment for the employee
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT numAffect, NouveauLieu 
            FROM AFFECTER 
            WHERE numEmp = ? 
            ORDER BY dateAffect DESC, datePriseService DESC
            LIMIT 1
        """, (assignment.numEmp,))
        
        latest_assignment = cursor.fetchone()
        
        # If this is the most recent assignment, we need to update the employee's location
        update_employee_location = (latest_assignment and 
                                  latest_assignment[0] == assignment_id and
                                  latest_assignment[1] != assignment.NouveauLieu)
        
        # Update in database
        try:
            cursor = self.db.conn.cursor()
            
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Update assignment
            cursor.execute("""
                UPDATE AFFECTER 
                SET numEmp = ?, AncienLieu = ?, NouveauLieu = ?, 
                    dateAffect = ?, datePriseService = ?
                WHERE numAffect = ?
            """, (
                assignment.numEmp, assignment.AncienLieu, assignment.NouveauLieu,
                assignment.dateAffect, assignment.datePriseService, assignment_id
            ))
            
            if cursor.rowcount == 0:
                self.db.conn.rollback()
                return False, "Assignment not found."
            
            # Update employee's current location if this is their most recent assignment
            if update_employee_location:
                cursor.execute(
                    "UPDATE EMPLOYE SET idlieu = ? WHERE numEmp = ?",
                    (assignment.NouveauLieu, assignment.numEmp)
                )
            
            self.db.conn.commit()
            return True, "Assignment updated successfully!"
            
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error updating assignment: {str(e)}"
    
    def delete(self, assignment_id: str) -> Tuple[bool, str]:
        """Delete an assignment.
        
        This will also update the employee's current location if this was their most recent assignment.
        
        Args:
            assignment_id: ID of the assignment to delete
            
        Returns:
            Tuple of (success, message)
        """
        # Get assignment
        assignment = self.get_by_id(assignment_id)
        if not assignment:
            return False, "Assignment not found."
        
        # Check if this is the most recent assignment for the employee
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT numAffect, NouveauLieu 
            FROM AFFECTER 
            WHERE numEmp = ? 
            ORDER BY dateAffect DESC, datePriseService DESC
            LIMIT 1
        """, (assignment.numEmp,))
        
        latest_assignment = cursor.fetchone()
        
        # If this is the most recent assignment, we need to update the employee's location
        update_employee_location = (latest_assignment and 
                                  latest_assignment[0] == assignment_id)
        
        # Delete from database
        try:
            cursor = self.db.conn.cursor()
            
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Delete assignment
            cursor.execute("DELETE FROM AFFECTER WHERE numAffect = ?", (assignment_id,))
            
            if cursor.rowcount == 0:
                self.db.conn.rollback()
                return False, "Assignment not found."
            
            # Update employee's current location if this was their most recent assignment
            if update_employee_location:
                # Get the new most recent assignment (if any)
                cursor.execute("""
                    SELECT NouveauLieu 
                    FROM AFFECTER 
                    WHERE numEmp = ?
                    ORDER BY dateAffect DESC, datePriseService DESC
                    LIMIT 1
                """, (assignment.numEmp,))
                
                result = cursor.fetchone()
                new_location = result[0] if result else None
                
                cursor.execute(
                    "UPDATE EMPLOYE SET idlieu = ? WHERE numEmp = ?",
                    (new_location, assignment.numEmp)
                )
            
            self.db.conn.commit()
            return True, "Assignment deleted successfully!"
            
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error deleting assignment: {str(e)}"
    
    def get_employee_assignments(
        self, 
        employee_id: str,
        limit: int = None
    ) -> List[Assignment]:
        """Get all assignments for a specific employee.
        
        Args:
            employee_id: Employee ID
            limit: Maximum number of assignments to return
            
        Returns:
            List of Assignment objects for the employee
        """
        return Assignment.get_employee_assignments(self.db, employee_id, limit=limit)
    
    def get_assignments_between_dates(
        self, 
        start_date: str, 
        end_date: str
    ) -> List[Assignment]:
        """Get all assignments between two dates.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of Assignment objects within the date range
        """
        return Assignment.get_assignments_between_dates(self.db, start_date, end_date)
    
    def get_recent_assignments(self, limit: int = 10) -> List[Assignment]:
        """Get the most recent assignments.
        
        Args:
            limit: Maximum number of assignments to return
            
        Returns:
            List of recent Assignment objects
        """
        return Assignment.get_recent_assignments(self.db, limit=limit)
    
    def get_employee_current_location(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Get an employee's current location information.
        
        Args:
            employee_id: Employee ID
            
        Returns:
            Dictionary with location information, or None if employee has no location
        """
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT e.idlieu, l.design, l.province
            FROM EMPLOYE e
            LEFT JOIN LIEU l ON e.idlieu = l.idlieu
            WHERE e.numEmp = ?
        """, (employee_id,))
        
        result = cursor.fetchone()
        if not result or not result[0]:
            return None
            
        return {
            'idlieu': result[0],
            'design': result[1],
            'province': result[2]
        }
