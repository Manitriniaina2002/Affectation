from datetime import date, datetime
from typing import Dict, List, Optional, Tuple, Any, TYPE_CHECKING

from .base_model import BaseModel

if TYPE_CHECKING:
    from .database import Database
    from .assignment import Assignment

class Employee(BaseModel):
    """Model representing an employee in the system."""
    
    TABLE_NAME = 'EMPLOYE'
    PRIMARY_KEY = 'numEmp'
    FIELDS = {
        'numEmp': 'TEXT',
        'civilite': 'TEXT',
        'nom': 'TEXT',
        'prenom': 'TEXT',
        'mail': 'TEXT',
        'poste': 'TEXT',
        'idlieu': 'TEXT'
    }
    
    # Valid civilite options
    CIVILITE_OPTIONS = ['Mr', 'Mme', 'Mlle']
    
    def __init__(
        self,
        numEmp: str = None,
        civilite: str = None,
        nom: str = None,
        prenom: str = None,
        mail: str = None,
        poste: str = None,
        idlieu: str = None,
        lieu_design: str = None,  # For joined data
        province: str = None      # For joined data
    ):
        """Initialize an Employee instance.
        
        Args:
            numEmp: Employee ID
            civilite: Title (Mr, Mme, Mlle)
            nom: Last name
            prenom: First name
            mail: Email address
            poste: Job position
            idlieu: Current location ID
            lieu_design: Location designation (for joined queries)
            province: Location province (for joined queries)
        """
        super().__init__()
        self.numEmp = numEmp
        self.civilite = civilite
        self.nom = nom
        self.prenom = prenom
        self.mail = mail
        self.poste = poste
        self.idlieu = idlieu
        self.lieu_design = lieu_design
        self.province = province
    
    @property
    def full_name(self) -> str:
        """Get the full name of the employee."""
        return f"{self.prenom} {self.nom}" if self.prenom and self.nom else self.numEmp
    
    def validate(self) -> Tuple[bool, str]:
        """Validate the employee data before saving.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not self.numEmp or not self.numEmp.strip():
            return False, "Employee ID is required."
        if not self.civilite or self.civilite not in self.CIVILITE_OPTIONS:
            return False, f"Valid title is required. Must be one of: {', '.join(self.CIVILITE_OPTIONS)}"
        if not self.nom or not self.nom.strip():
            return False, "Last name is required."
        if not self.prenom or not self.prenom.strip():
            return False, "First name is required."
        if not self.mail or '@' not in self.mail:
            return False, "Valid email address is required."
        if not self.poste or not self.poste.strip():
            return False, "Job position is required."
        return True, ""
    
    def get_current_location(self, db: 'Database') -> Optional['Location']:
        """Get the employee's current location.
        
        Args:
            db: Database connection
            
        Returns:
            Optional[Location]: The employee's current location, or None if not assigned
        """
        if not self.idlieu:
            return None
            
        from .location import Location
        return Location.get(db, self.idlieu)
    
    def get_assignments(
        self, 
        db: 'Database',
        limit: int = None,
        order_by: str = 'dateAffect DESC, datePriseService DESC'
    ) -> List['Assignment']:
        """Get all assignments for this employee.
        
        Args:
            db: Database connection
            limit: Maximum number of assignments to return
            order_by: SQL ORDER BY clause (without the ORDER BY keywords)
            
        Returns:
            List[Assignment]: List of assignments for this employee
        """
        from .assignment import Assignment
        
        query = f"""
            SELECT * FROM {Assignment.TABLE_NAME}
            WHERE numEmp = ?
            ORDER BY {order_by}
            {f'LIMIT {limit}' if limit else ''}
        """
        
        cursor = db.conn.cursor()
        cursor.execute(query, (self.numEmp,))
        
        return [Assignment.from_row(row) for row in cursor.fetchall()]
    
    def get_latest_assignment(self, db: 'Database') -> Optional['Assignment']:
        """Get the most recent assignment for this employee.
        
        Args:
            db: Database connection
            
        Returns:
            Optional[Assignment]: The most recent assignment, or None if none exists
        """
        assignments = self.get_assignments(db, limit=1)
        return assignments[0] if assignments else None
    
    def is_currently_assigned(self, db: 'Database') -> bool:
        """Check if the employee is currently assigned to a location.
        
        Args:
            db: Database connection
            
        Returns:
            bool: True if the employee has a current location assignment
        """
        return self.idlieu is not None
    
    @classmethod
    def search(
        cls, 
        db: 'Database',
        search_term: str = None,
        location_id: str = None,
        position: str = None,
        province: str = None
    ) -> List['Employee']:
        """Search employees with various filters.
        
        Args:
            db: Database connection
            search_term: Term to search in name, email, or employee ID
            location_id: Filter by current location ID
            position: Filter by job position (partial match)
            province: Filter by location province
            
        Returns:
            List[Employee]: List of matching employees
        """
        query = f"""
            SELECT e.*, l.design as lieu_design, l.province 
            FROM {cls.TABLE_NAME} e
            LEFT JOIN LIEU l ON e.idlieu = l.idlieu
            WHERE 1=1
        """
        
        params = []
        
        if search_term:
            query += " AND (e.nom LIKE ? OR e.prenom LIKE ? OR e.mail LIKE ? OR e.numEmp LIKE ?)"
            search_param = f"%{search_term}%"
            params.extend([search_param] * 4)
        
        if location_id:
            query += " AND e.idlieu = ?"
            params.append(location_id)
            
        if position:
            query += " AND e.poste LIKE ?"
            params.append(f"%{position}%")
            
        if province:
            query += " AND l.province = ?"
            params.append(province)
        
        query += " ORDER BY e.nom, e.prenom"
        
        cursor = db.conn.cursor()
        cursor.execute(query, params)
        
        return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_unassigned(cls, db: 'Database') -> List['Employee']:
        """Get all employees who don't have a current location assignment.
        
        Args:
            db: Database connection
            
        Returns:
            List[Employee]: List of unassigned employees
        """
        query = f"""
            SELECT * FROM {cls.TABLE_NAME}
            WHERE idlieu IS NULL
            ORDER BY nom, prenom
        """
        
        cursor = db.conn.cursor()
        cursor.execute(query)
        
        return [cls.from_row(row) for row in cursor.fetchall()]
