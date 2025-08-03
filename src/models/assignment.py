from datetime import date, datetime
from typing import Dict, List, Optional, Tuple, Any, TYPE_CHECKING

from .base_model import BaseModel

if TYPE_CHECKING:
    from .database import Database
    from .employee import Employee
    from .location import Location

class Assignment(BaseModel):
    """Model representing an employee assignment in the system."""
    
    TABLE_NAME = 'AFFECTER'
    PRIMARY_KEY = 'numAffect'
    FIELDS = {
        'numAffect': 'TEXT',
        'numEmp': 'TEXT',
        'AncienLieu': 'TEXT',
        'NouveauLieu': 'TEXT',
        'dateAffect': 'DATE',
        'datePriseService': 'DATE'
    }
    
    def __init__(
        self,
        numAffect: str = None,
        numEmp: str = None,
        AncienLieu: str = None,
        NouveauLieu: str = None,
        dateAffect: str = None,
        datePriseService: str = None,
        # Joined fields (not part of the main table)
        civilite: str = None,
        nom: str = None,
        prenom: str = None,
        poste: str = None,
        ancien_lieu_design: str = None,
        ancien_province: str = None,
        nouveau_lieu_design: str = None,
        nouveau_province: str = None
    ):
        """Initialize an Assignment instance.
        
        Args:
            numAffect: Assignment ID
            numEmp: Employee ID
            AncienLieu: Previous location ID
            NouveauLieu: New location ID
            dateAffect: Assignment date (YYYY-MM-DD)
            datePriseService: Start date of service (YYYY-MM-DD)
            
            # The following are for joined data and not part of the main table
            civilite: Employee's title (from join)
            nom: Employee's last name (from join)
            prenom: Employee's first name (from join)
            poste: Employee's position (from join)
            ancien_lieu_design: Previous location name (from join)
            ancien_province: Previous location province (from join)
            nouveau_lieu_design: New location name (from join)
            nouveau_province: New location province (from join)
        """
        super().__init__()
        self.numAffect = numAffect
        self.numEmp = numEmp
        self.AncienLieu = AncienLieu
        self.NouveauLieu = NouveauLieu
        self.dateAffect = dateAffect
        self.datePriseService = datePriseService
        
        # Joined fields
        self.civilite = civilite
        self.nom = nom
        self.prenom = prenom
        self.poste = poste
        self.ancien_lieu_design = ancien_lieu_design
        self.ancien_province = ancien_province
        self.nouveau_lieu_design = nouveau_lieu_design
        self.nouveau_province = nouveau_province
    
    @property
    def employee_name(self) -> str:
        """Get the full name of the employee."""
        if self.prenom and self.nom:
            return f"{self.prenom} {self.nom}"
        return self.numEmp or "Unknown"
    
    @property
    def ancien_lieu(self) -> str:
        """Get a formatted string of the previous location."""
        if self.ancien_lieu_design and self.ancien_province:
            return f"{self.ancien_lieu_design} ({self.ancien_province})"
        return self.AncienLieu or "N/A"
    
    @property
    def nouveau_lieu(self) -> str:
        """Get a formatted string of the new location."""
        if self.nouveau_lieu_design and self.nouveau_province:
            return f"{self.nouveau_lieu_design} ({self.nouveau_province})"
        return self.NouveauLieu or "N/A"
    
    def validate(self) -> Tuple[bool, str]:
        """Validate the assignment data before saving.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not self.numAffect or not self.numAffect.strip():
            return False, "Assignment ID is required."
        if not self.numEmp or not self.numEmp.strip():
            return False, "Employee is required."
        if not self.AncienLieu or not self.AncienLieu.strip():
            return False, "Previous location is required."
        if not self.NouveauLieu or not self.NouveauLieu.strip():
            return False, "New location is required."
        if self.AncienLieu == self.NouveauLieu:
            return False, "Previous and new locations must be different."
        
        try:
            # Validate date formats
            affect_date = datetime.strptime(self.dateAffect, '%Y-%m-%d').date()
            service_date = datetime.strptime(self.datePriseService, '%Y-%m-%d').date()
            
            # Check that service date is not before assignment date
            if service_date < affect_date:
                return False, "Service start date cannot be before assignment date."
                
            # Check that assignment date is not in the future
            if affect_date > date.today():
                return False, "Assignment date cannot be in the future."
                
        except ValueError as e:
            return False, f"Invalid date format. Please use YYYY-MM-DD: {str(e)}"
            
        return True, ""
    
    def get_employee(self, db: 'Database') -> Optional['Employee']:
        """Get the employee associated with this assignment.
        
        Args:
            db: Database connection
            
        Returns:
            Optional[Employee]: The employee, or None if not found
        """
        if not self.numEmp:
            return None
            
        from .employee import Employee
        return Employee.get(db, self.numEmp)
    
    def get_old_location(self, db: 'Database') -> Optional['Location']:
        """Get the previous location.
        
        Args:
            db: Database connection
            
        Returns:
            Optional[Location]: The previous location, or None if not found
        """
        if not self.AncienLieu:
            return None
            
        from .location import Location
        return Location.get(db, self.AncienLieu)
    
    def get_new_location(self, db: 'Database') -> Optional['Location']:
        """Get the new location.
        
        Args:
            db: Database connection
            
        Returns:
            Optional[Location]: The new location, or None if not found
        """
        if not self.NouveauLieu:
            return None
            
        from .location import Location
        return Location.get(db, self.NouveauLieu)
    
    @classmethod
    def get_employee_assignments(
        cls, 
        db: 'Database', 
        numEmp: str,
        limit: int = None,
        order_by: str = 'dateAffect DESC, datePriseService DESC'
    ) -> List['Assignment']:
        """Get all assignments for a specific employee.
        
        Args:
            db: Database connection
            numEmp: Employee ID
            limit: Maximum number of assignments to return
            order_by: SQL ORDER BY clause (without the ORDER BY keywords)
            
        Returns:
            List[Assignment]: List of assignments for the employee
        """
        query = f"""
            SELECT a.*, 
                   al.design as ancien_lieu_design, al.province as ancien_province,
                   nl.design as nouveau_lieu_design, nl.province as nouveau_province
            FROM {cls.TABLE_NAME} a
            JOIN LIEU al ON a.AncienLieu = al.idlieu
            JOIN LIEU nl ON a.NouveauLieu = nl.idlieu
            WHERE a.numEmp = ?
            ORDER BY {order_by}
            {f'LIMIT {limit}' if limit else ''}
        """
        
        cursor = db.conn.cursor()
        cursor.execute(query, (numEmp,))
        
        return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_between_dates(
        cls, 
        db: 'Database',
        start_date: str,
        end_date: str,
        order_by: str = 'a.dateAffect, a.datePriseService'
    ) -> List['Assignment']:
        """Get all assignments between two dates.
        
        Args:
            db: Database connection
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            order_by: SQL ORDER BY clause (without the ORDER BY keywords)
            
        Returns:
            List[Assignment]: List of assignments between the specified dates
        """
        query = f"""
            SELECT a.*, 
                   e.civilite, e.nom, e.prenom, e.poste,
                   al.design as ancien_lieu_design, al.province as ancien_province,
                   nl.design as nouveau_lieu_design, nl.province as nouveau_province
            FROM {cls.TABLE_NAME} a
            JOIN EMPLOYE e ON a.numEmp = e.numEmp
            JOIN LIEU al ON a.AncienLieu = al.idlieu
            JOIN LIEU nl ON a.NouveauLieu = nl.idlieu
            WHERE a.dateAffect BETWEEN ? AND ?
            ORDER BY {order_by}
        """
        
        cursor = db.conn.cursor()
        cursor.execute(query, (start_date, end_date))
        
        return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_recent_assignments(
        cls, 
        db: 'Database', 
        limit: int = 10,
        order_by: str = 'a.dateAffect DESC, a.datePriseService DESC'
    ) -> List['Assignment']:
        """Get the most recent assignments.
        
        Args:
            db: Database connection
            limit: Maximum number of assignments to return
            order_by: SQL ORDER BY clause (without the ORDER BY keywords)
            
        Returns:
            List[Assignment]: List of recent assignments
        """
        query = f"""
            SELECT a.*, 
                   e.civilite, e.nom, e.prenom, e.poste,
                   al.design as ancien_lieu_design, al.province as ancien_province,
                   nl.design as nouveau_lieu_design, nl.province as nouveau_province
            FROM {cls.TABLE_NAME} a
            JOIN EMPLOYE e ON a.numEmp = e.numEmp
            JOIN LIEU al ON a.AncienLieu = al.idlieu
            JOIN LIEU nl ON a.NouveauLieu = nl.idlieu
            ORDER BY {order_by}
            LIMIT ?
        """
        
        cursor = db.conn.cursor()
        cursor.execute(query, (limit,))
        
        return [cls.from_row(row) for row in cursor.fetchall()]
