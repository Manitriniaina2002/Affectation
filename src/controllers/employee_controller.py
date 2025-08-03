"""
Employee controller for the Employee Assignment Management System.
This module handles all business logic related to employees.
"""
from typing import Any, Dict, List, Optional, Tuple

from ..models.employee import Employee
from ..models.location import Location
from .base_controller import BaseController

class EmployeeController(BaseController):
    """Controller for employee-related operations."""
    
    def get_all(self, **kwargs) -> List[Employee]:
        """Get all employees with their current location information.
        
        Args:
            **kwargs: Additional filters/parameters
                - location_id: Filter by current location ID
                - unassigned: If True, only return employees without a location
                
        Returns:
            List of Employee objects
        """
        location_id = kwargs.get('location_id')
        unassigned = kwargs.get('unassigned', False)
        
        if unassigned:
            return self.get_unassigned_employees()
        
        if location_id:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT e.*, l.design as lieu_design, l.province 
                FROM EMPLOYE e
                LEFT JOIN LIEU l ON e.idlieu = l.idlieu
                WHERE e.idlieu = ?
                ORDER BY e.nom, e.prenom
            """, (location_id,))
        else:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT e.*, l.design as lieu_design, l.province 
                FROM EMPLOYE e
                LEFT JOIN LIEU l ON e.idlieu = l.idlieu
                ORDER BY e.nom, e.prenom
            """)
            
        return [Employee.from_row(row) for row in cursor.fetchall()]
    
    def get_by_id(self, employee_id: str) -> Optional[Employee]:
        """Get an employee by ID with location information.
        
        Args:
            employee_id: Employee ID
            
        Returns:
            Employee object with location info, or None if not found
        """
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT e.*, l.design as lieu_design, l.province 
            FROM EMPLOYE e
            LEFT JOIN LIEU l ON e.idlieu = l.idlieu
            WHERE e.numEmp = ?
        """, (employee_id,))
        
        row = cursor.fetchone()
        return Employee.from_row(row) if row else None
    
    def create(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Create a new employee.
        
        Args:
            data: Employee data with keys:
                - numEmp: Employee ID (optional, will be generated if not provided)
                - civilite: Title (Mr, Mme, Mlle)
                - nom: Last name
                - prenom: First name
                - mail: Email address
                - poste: Job position
                - idlieu: Current location ID (optional)
                
        Returns:
            Tuple of (success, message, employee_id)
        """
        # Validate required fields
        required_fields = ['civilite', 'nom', 'prenom', 'mail', 'poste']
        is_valid, error_msg = self._validate_required_fields(data, required_fields)
        if not is_valid:
            return False, error_msg, None
        
        # Generate employee ID if not provided
        if 'numEmp' not in data or not data['numEmp']:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT numEmp FROM EMPLOYE")
            existing_ids = [row[0] for row in cursor.fetchall()]
            data['numEmp'] = self._get_next_id('E', existing_ids)
        
        # Create employee object
        employee = Employee(
            numEmp=data['numEmp'].strip(),
            civilite=data['civilite'].strip(),
            nom=data['nom'].strip(),
            prenom=data['prenom'].strip(),
            mail=data['mail'].strip().lower(),
            poste=data['poste'].strip(),
            idlieu=data.get('idlieu')
        )
        
        # Validate employee
        is_valid, error_msg = employee.validate()
        if not is_valid:
            return False, error_msg, None
        
        # Check if location exists if provided
        if employee.idlieu:
            location = Location.get(self.db, employee.idlieu)
            if not location:
                return False, f"Location with ID '{employee.idlieu}' not found.", None
        
        # Check if email already exists
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM EMPLOYE WHERE mail = ?",
            (employee.mail,)
        )
        if cursor.fetchone()[0] > 0:
            return False, f"An employee with email '{employee.mail}' already exists.", None
        
        # Save to database
        try:
            cursor.execute("""
                INSERT INTO EMPLOYE (numEmp, civilite, nom, prenom, mail, poste, idlieu)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                employee.numEmp, employee.civilite, employee.nom, 
                employee.prenom, employee.mail, employee.poste, employee.idlieu
            ))
            
            self.db.conn.commit()
            return True, "Employee created successfully!", employee.numEmp
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error creating employee: {str(e)}", None
    
    def update(self, employee_id: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update an existing employee.
        
        Args:
            employee_id: ID of the employee to update
            data: Updated employee data with keys:
                - civilite: Title (Mr, Mme, Mlle)
                - nom: Last name
                - prenom: First name
                - mail: Email address
                - poste: Job position
                - idlieu: Current location ID (set to None to unassign)
                
        Returns:
            Tuple of (success, message)
        """
        # Get existing employee
        employee = self.get_by_id(employee_id)
        if not employee:
            return False, "Employee not found."
        
        # Update fields
        if 'civilite' in data:
            employee.civilite = data['civilite'].strip()
        if 'nom' in data:
            employee.nom = data['nom'].strip()
        if 'prenom' in data:
            employee.prenom = data['prenom'].strip()
        if 'mail' in data:
            employee.mail = data['mail'].strip().lower()
        if 'poste' in data:
            employee.poste = data['poste'].strip()
        if 'idlieu' in data:
            employee.idlieu = data['idlieu'] if data['idlieu'] else None
        
        # Validate employee
        is_valid, error_msg = employee.validate()
        if not is_valid:
            return False, error_msg
        
        # Check if location exists if provided
        if employee.idlieu:
            location = Location.get(self.db, employee.idlieu)
            if not location:
                return False, f"Location with ID '{employee.idlieu}' not found."
        
        # Check if email already exists (for another employee)
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM EMPLOYE WHERE mail = ? AND numEmp != ?",
            (employee.mail, employee_id)
        )
        if cursor.fetchone()[0] > 0:
            return False, f"Another employee with email '{employee.mail}' already exists."
        
        # Update in database
        try:
            cursor.execute("""
                UPDATE EMPLOYE 
                SET civilite = ?, nom = ?, prenom = ?, 
                    mail = ?, poste = ?, idlieu = ?
                WHERE numEmp = ?
            """, (
                employee.civilite, employee.nom, employee.prenom,
                employee.mail, employee.poste, employee.idlieu,
                employee_id
            ))
            
            if cursor.rowcount == 0:
                return False, "Employee not found."
                
            self.db.conn.commit()
            return True, "Employee updated successfully!"
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error updating employee: {str(e)}"
    
    def delete(self, employee_id: str) -> Tuple[bool, str]:
        """Delete an employee.
        
        Args:
            employee_id: ID of the employee to delete
            
        Returns:
            Tuple of (success, message)
        """
        # Check if employee exists
        employee = self.get_by_id(employee_id)
        if not employee:
            return False, "Employee not found."
        
        # Check if employee has assignments
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM AFFECTER WHERE numEmp = ?",
            (employee_id,)
        )
        if cursor.fetchone()[0] > 0:
            return False, "Cannot delete employee: Employee has assignment history."
        
        # Delete employee
        try:
            cursor.execute("DELETE FROM EMPLOYE WHERE numEmp = ?", (employee_id,))
            
            if cursor.rowcount == 0:
                return False, "Employee not found."
                
            self.db.conn.commit()
            return True, "Employee deleted successfully!"
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error deleting employee: {str(e)}"
    
    def search_employees(
        self,
        search_term: str = None,
        location_id: str = None,
        position: str = None,
        province: str = None
    ) -> List[Employee]:
        """Search employees with various filters.
        
        Args:
            search_term: Term to search in name, email, or employee ID
            location_id: Filter by current location ID
            position: Filter by job position (partial match)
            province: Filter by location province
            
        Returns:
            List of matching Employee objects
        """
        return Employee.search(
            self.db,
            search_term=search_term,
            location_id=location_id,
            position=position,
            province=province
        )
    
    def get_unassigned_employees(self) -> List[Employee]:
        """Get all employees who don't have a current location assignment.
        
        Returns:
            List of unassigned Employee objects
        """
        return Employee.get_unassigned(self.db)
    
    def assign_location(
        self,
        employee_id: str,
        new_location_id: str,
        assignment_date: str,
        service_start_date: str,
        assignment_id: str = None
    ) -> Tuple[bool, str]:
        """Assign an employee to a new location.
        
        This creates a new assignment record and updates the employee's current location.
        
        Args:
            employee_id: ID of the employee to assign
            new_location_id: ID of the new location
            assignment_date: Assignment date (YYYY-MM-DD)
            service_start_date: Service start date (YYYY-MM-DD)
            assignment_id: Optional assignment ID (will be generated if not provided)
            
        Returns:
            Tuple of (success, message)
        """
        # Get employee and validate
        employee = self.get_by_id(employee_id)
        if not employee:
            return False, "Employee not found."
        
        # Get new location and validate
        new_location = Location.get(self.db, new_location_id)
        if not new_location:
            return False, f"Location with ID '{new_location_id}' not found."
        
        # Check if assignment would be redundant
        if employee.idlieu == new_location_id:
            return False, f"Employee is already assigned to {new_location.design}."
        
        # Get old location (if any)
        old_location_id = employee.idlieu or 'UNKNOWN'
        
        # Generate assignment ID if not provided
        if not assignment_id:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT numAffect FROM AFFECTER")
            existing_ids = [row[0] for row in cursor.fetchall()]
            assignment_id = self._get_next_id('A', existing_ids)
        
        # Create assignment in database
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
                assignment_id, employee_id, old_location_id,
                new_location_id, assignment_date, service_start_date
            ))
            
            # Update employee's current location
            cursor.execute(
                "UPDATE EMPLOYE SET idlieu = ? WHERE numEmp = ?",
                (new_location_id, employee_id)
            )
            
            self.db.conn.commit()
            return True, f"Employee assigned to {new_location.design} successfully!"
            
        except Exception as e:
            self.db.conn.rollback()
            return False, f"Error assigning location: {str(e)}"
