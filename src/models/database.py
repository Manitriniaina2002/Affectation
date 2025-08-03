import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file='employee_assignments.db'):
        """Initialize the database connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
        self.seed_initial_data()
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Create LIEU (LOCATION) table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS LIEU (
            idlieu TEXT PRIMARY KEY,
            design TEXT NOT NULL,
            province TEXT NOT NULL
        )
        ''')
        
        # Create EMPLOYE (EMPLOYEE) table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS EMPLOYE (
            numEmp TEXT PRIMARY KEY,
            civilite TEXT CHECK(civilite IN ('Mr', 'Mme', 'Mlle')) NOT NULL,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            mail TEXT UNIQUE NOT NULL,
            poste TEXT NOT NULL,
            idlieu TEXT,
            FOREIGN KEY (idlieu) REFERENCES LIEU(idlieu)
        )
        ''')
        
        # Create AFFECTER (ASSIGNMENT) table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS AFFECTER (
            numAffect TEXT PRIMARY KEY,
            numEmp TEXT NOT NULL,
            AncienLieu TEXT NOT NULL,
            NouveauLieu TEXT NOT NULL,
            dateAffect DATE NOT NULL,
            datePriseService DATE NOT NULL,
            FOREIGN KEY (numEmp) REFERENCES EMPLOYE(numEmp),
            FOREIGN KEY (AncienLieu) REFERENCES LIEU(idlieu),
            FOREIGN KEY (NouveauLieu) REFERENCES LIEU(idlieu)
        )
        ''')
        
        self.conn.commit()
    
    def seed_initial_data(self):
        """Seed the database with initial sample data if tables are empty."""
        cursor = self.conn.cursor()
        
        # Check if LIEU table is empty
        cursor.execute("SELECT COUNT(*) FROM LIEU")
        if cursor.fetchone()[0] == 0:
            # Sample locations
            locations = [
                ('L1', 'Antananarivo', 'Antananarivo'),
                ('L2', 'Toamasina', 'Toamasina'),
                ('L3', 'Antsirabe', 'Antananarivo'),
                ('L4', 'Fianarantsoa', 'Fianarantsoa'),
                ('L5', 'Mahajanga', 'Mahajanga'),
                ('L6', 'Toliara', 'Toliara'),
                ('L7', 'Antsiranana', 'Antsiranana'),
                ('L8', 'Moramanga', 'Toamasina'),
                ('L9', 'Ambalavao', 'Fianarantsoa'),
                ('L10', 'Sambava', 'Antsiranana')
            ]
            cursor.executemany("INSERT INTO LIEU (idlieu, design, province) VALUES (?, ?, ?)", locations)
        
        # Check if EMPLOYE table is empty
        cursor.execute("SELECT COUNT(*) FROM EMPLOYE")
        if cursor.fetchone()[0] == 0:
            # Sample employees
            employees = [
                ('E001', 'Mr', 'Rakoto', 'Jean', 'jean.rakoto@example.com', 'Manager', 'L1'),
                ('E002', 'Mme', 'Rasoa', 'Marie', 'marie.rasoa@example.com', 'Developer', 'L1'),
                ('E003', 'Mr', 'Rabe', 'Paul', 'paul.rabe@example.com', 'Analyst', 'L2'),
                ('E004', 'Mlle', 'Rakotomalala', 'Sofia', 'sofia.rakoto@example.com', 'Designer', 'L3'),
                ('E005', 'Mr', 'Randria', 'Jean', 'jean.randria@example.com', 'Tester', 'L4'),
                ('E006', 'Mme', 'Razafy', 'Claire', 'claire.razafy@example.com', 'Developer', 'L2'),
                ('E007', 'Mr', 'Rakotondrabe', 'Marc', 'marc.rabe@example.com', 'Manager', 'L5'),
                ('E008', 'Mlle', 'Rasolofoniaina', 'Julie', 'julie.rasolo@example.com', 'Analyst', 'L6'),
                ('E009', 'Mr', 'Randriamanantena', 'Pierre', 'pierre.randria@example.com', 'Developer', 'L7'),
                ('E010', 'Mme', 'Rakotovao', 'Nirina', 'nirina.rakoto@example.com', 'Designer', 'L8')
            ]
            cursor.executemany("""
                INSERT INTO EMPLOYE (numEmp, civilite, nom, prenom, mail, poste, idlieu)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, employees)
        
        # Check if AFFECTER table is empty
        cursor.execute("SELECT COUNT(*) FROM AFFECTER")
        if cursor.fetchone()[0] == 0:
            # Sample assignments
            assignments = [
                ('A001', 'E001', 'L1', 'L2', '2023-01-15', '2023-02-01'),
                ('A002', 'E002', 'L1', 'L3', '2023-02-10', '2023-02-20'),
                ('A003', 'E003', 'L2', 'L4', '2023-03-05', '2023-03-15'),
                ('A004', 'E004', 'L3', 'L5', '2023-04-12', '2023-04-22'),
                ('A005', 'E005', 'L4', 'L6', '2023-05-20', '2023-06-01'),
                ('A006', 'E006', 'L2', 'L7', '2023-06-15', '2023-06-25'),
                ('A007', 'E007', 'L5', 'L8', '2023-07-10', '2023-07-20'),
                ('A008', 'E008', 'L6', 'L9', '2023-08-05', '2023-08-15'),
                ('A009', 'E009', 'L7', 'L10', '2023-09-12', '2023-09-22'),
                ('A010', 'E010', 'L8', 'L1', '2023-10-18', '2023-11-01')
            ]
            cursor.executemany("""
                INSERT INTO AFFECTER (numAffect, numEmp, AncienLieu, NouveauLieu, dateAffect, datePriseService)
                VALUES (?, ?, ?, ?, ?, ?)
            """, assignments)
        
        self.conn.commit()
    
    def close(self):
        """Close the database connection."""
        self.conn.close()
    
    # Location methods
    def add_location(self, idlieu, design, province):
        """Add a new location to the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO LIEU (idlieu, design, province) VALUES (?, ?, ?)",
                (idlieu, design, province)
            )
            self.conn.commit()
            return True, "Location added successfully!"
        except sqlite3.IntegrityError as e:
            return False, f"Error adding location: {str(e)}"
    
    def update_location(self, idlieu, design, province):
        """Update an existing location."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE LIEU SET design = ?, province = ? WHERE idlieu = ?",
                (design, province, idlieu)
            )
            self.conn.commit()
            if cursor.rowcount > 0:
                return True, "Location updated successfully!"
            else:
                return False, "Location not found!"
        except Exception as e:
            return False, f"Error updating location: {str(e)}"
    
    def delete_location(self, idlieu):
        """Delete a location from the database."""
        try:
            cursor = self.conn.cursor()
            
            # Check if location is referenced in EMPLOYE or AFFECTER tables
            cursor.execute("SELECT COUNT(*) FROM EMPLOYE WHERE idlieu = ?", (idlieu,))
            if cursor.fetchone()[0] > 0:
                return False, "Cannot delete location: Employees are assigned to this location."
                
            cursor.execute("SELECT COUNT(*) FROM AFFECTER WHERE AncienLieu = ? OR NouveauLieu = ?", 
                          (idlieu, idlieu))
            if cursor.fetchone()[0] > 0:
                return False, "Cannot delete location: Location is referenced in assignment history."
            
            cursor.execute("DELETE FROM LIEU WHERE idlieu = ?", (idlieu,))
            self.conn.commit()
            
            if cursor.rowcount > 0:
                return True, "Location deleted successfully!"
            else:
                return False, "Location not found!"
        except Exception as e:
            return False, f"Error deleting location: {str(e)}"
    
    def get_all_locations(self):
        """Get all locations from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM LIEU ORDER BY province, design")
        return cursor.fetchall()
    
    def get_location(self, idlieu):
        """Get a single location by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM LIEU WHERE idlieu = ?", (idlieu,))
        return cursor.fetchone()
    
    # Employee methods
    def add_employee(self, numEmp, civilite, nom, prenom, mail, poste, idlieu=None):
        """Add a new employee to the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO EMPLOYE (numEmp, civilite, nom, prenom, mail, poste, idlieu)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (numEmp, civilite, nom, prenom, mail, poste, idlieu))
            self.conn.commit()
            return True, "Employee added successfully!"
        except sqlite3.IntegrityError as e:
            return False, f"Error adding employee: {str(e)}"
    
    def update_employee(self, numEmp, civilite, nom, prenom, mail, poste, idlieu):
        """Update an existing employee."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE EMPLOYE 
                SET civilite = ?, nom = ?, prenom = ?, mail = ?, poste = ?, idlieu = ?
                WHERE numEmp = ?
            """, (civilite, nom, prenom, mail, poste, idlieu, numEmp))
            self.conn.commit()
            if cursor.rowcount > 0:
                return True, "Employee updated successfully!"
            else:
                return False, "Employee not found!"
        except Exception as e:
            return False, f"Error updating employee: {str(e)}"
    
    def delete_employee(self, numEmp):
        """Delete an employee from the database."""
        try:
            cursor = self.conn.cursor()
            
            # Check if employee has assignments
            cursor.execute("SELECT COUNT(*) FROM AFFECTER WHERE numEmp = ?", (numEmp,))
            if cursor.fetchone()[0] > 0:
                return False, "Cannot delete employee: Employee has assignment history."
            
            cursor.execute("DELETE FROM EMPLOYE WHERE numEmp = ?", (numEmp,))
            self.conn.commit()
            
            if cursor.rowcount > 0:
                return True, "Employee deleted successfully!"
            else:
                return False, "Employee not found!"
        except Exception as e:
            return False, f"Error deleting employee: {str(e)}"
    
    def get_all_employees(self):
        """Get all employees with their location information."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT e.*, l.design as lieu_design, l.province 
            FROM EMPLOYE e
            LEFT JOIN LIEU l ON e.idlieu = l.idlieu
            ORDER BY e.nom, e.prenom
        """)
        return cursor.fetchall()
    
    def get_employee(self, numEmp):
        """Get a single employee by ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT e.*, l.design as lieu_design, l.province 
            FROM EMPLOYE e
            LEFT JOIN LIEU l ON e.idlieu = l.idlieu
            WHERE e.numEmp = ?
        """, (numEmp,))
        return cursor.fetchone()
    
    # Assignment methods
    def add_assignment(self, numAffect, numEmp, ancien_lieu, nouveau_lieu, date_affect, date_prise_service):
        """Add a new assignment to the database."""
        try:
            cursor = self.conn.cursor()
            
            # Start transaction
            self.conn.execute("BEGIN TRANSACTION")
            
            # Add the assignment
            cursor.execute("""
                INSERT INTO AFFECTER (numAffect, numEmp, AncienLieu, NouveauLieu, dateAffect, datePriseService)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (numAffect, numEmp, ancien_lieu, nouveau_lieu, date_affect, date_prise_service))
            
            # Update employee's current location
            cursor.execute("""
                UPDATE EMPLOYE 
                SET idlieu = ? 
                WHERE numEmp = ?
            """, (nouveau_lieu, numEmp))
            
            self.conn.commit()
            return True, "Assignment added and employee location updated successfully!"
            
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            return False, f"Error adding assignment: {str(e)}"
        except Exception as e:
            self.conn.rollback()
            return False, f"An error occurred: {str(e)}"
    
    def update_assignment(self, numAffect, numEmp, ancien_lieu, nouveau_lieu, date_affect, date_prise_service):
        """Update an existing assignment."""
        try:
            cursor = self.conn.cursor()
            
            # Start transaction
            self.conn.execute("BEGIN TRANSACTION")
            
            # Get the original assignment to check if employee changed
            cursor.execute("""
                SELECT numEmp, NouveauLieu 
                FROM AFFECTER 
                WHERE numAffect = ?
            """, (numAffect,))
            
            original = cursor.fetchone()
            if not original:
                self.conn.rollback()
                return False, "Assignment not found!"
                
            original_emp, original_nouveau_lieu = original
            
            # Update the assignment
            cursor.execute("""
                UPDATE AFFECTER 
                SET numEmp = ?, AncienLieu = ?, NouveauLieu = ?, 
                    dateAffect = ?, datePriseService = ?
                WHERE numAffect = ?
            """, (numEmp, ancien_lieu, nouveau_lieu, date_affect, date_prise_service, numAffect))
            
            # If employee changed or location changed, update employee's current location
            if numEmp != original_emp or nouveau_lieu != original_nouveau_lieu:
                cursor.execute("""
                    UPDATE EMPLOYE 
                    SET idlieu = ? 
                    WHERE numEmp = ?
                """, (nouveau_lieu, numEmp))
            
            self.conn.commit()
            return True, "Assignment updated successfully!"
            
        except Exception as e:
            self.conn.rollback()
            return False, f"Error updating assignment: {str(e)}"
    
    def delete_assignment(self, numAffect):
        """Delete an assignment from the database."""
        try:
            cursor = self.conn.cursor()
            
            # Start transaction
            self.conn.execute("BEGIN TRANSACTION")
            
            # Get the assignment to find the employee and new location
            cursor.execute("""
                SELECT numEmp, NouveauLieu 
                FROM AFFECTER 
                WHERE numAffect = ?
            """, (numAffect,))
            
            assignment = cursor.fetchone()
            if not assignment:
                self.conn.rollback()
                return False, "Assignment not found!"
                
            numEmp, nouveau_lieu = assignment
            
            # Delete the assignment
            cursor.execute("DELETE FROM AFFECTER WHERE numAffect = ?", (numAffect,))
            
            # Get the most recent assignment for this employee (if any)
            cursor.execute("""
                SELECT NouveauLieu 
                FROM AFFECTER 
                WHERE numEmp = ? AND numAffect != ?
                ORDER BY dateAffect DESC, datePriseService DESC
                LIMIT 1
            """, (numEmp, numAffect))
            
            # Update employee's current location to the previous assignment's new location,
            # or NULL if no other assignments exist
            if cursor.fetchone():
                cursor.execute("""
                    SELECT NouveauLieu 
                    FROM AFFECTER 
                    WHERE numEmp = ? AND numAffect != ?
                    ORDER BY dateAffect DESC, datePriseService DESC
                    LIMIT 1
                """, (numEmp, numAffect))
                
                prev_nouveau_lieu = cursor.fetchone()[0]
                cursor.execute("""
                    UPDATE EMPLOYE 
                    SET idlieu = ? 
                    WHERE numEmp = ?
                """, (prev_nouveau_lieu, numEmp))
            else:
                cursor.execute("""
                    UPDATE EMPLOYE 
                    SET idlieu = NULL 
                    WHERE numEmp = ?
                """, (numEmp,))
            
            self.conn.commit()
            return True, "Assignment deleted and employee location updated!"
            
        except Exception as e:
            self.conn.rollback()
            return False, f"Error deleting assignment: {str(e)}"
    
    def get_all_assignments(self):
        """Get all assignments with employee and location details."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.*, 
                   e.civilite, e.nom, e.prenom, e.poste,
                   al.design as ancien_lieu_design, al.province as ancien_province,
                   nl.design as nouveau_lieu_design, nl.province as nouveau_province
            FROM AFFECTER a
            JOIN EMPLOYE e ON a.numEmp = e.numEmp
            JOIN LIEU al ON a.AncienLieu = al.idlieu
            JOIN LIEU nl ON a.NouveauLieu = nl.idlieu
            ORDER BY a.dateAffect DESC, a.datePriseService DESC
        """)
        return cursor.fetchall()
    
    def get_assignment(self, numAffect):
        """Get a single assignment by ID."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.*, 
                   e.civilite, e.nom, e.prenom, e.poste,
                   al.design as ancien_lieu_design, al.province as ancien_province,
                   nl.design as nouveau_lieu_design, nl.province as nouveau_province
            FROM AFFECTER a
            JOIN EMPLOYE e ON a.numEmp = e.numEmp
            JOIN LIEU al ON a.AncienLieu = al.idlieu
            JOIN LIEU nl ON a.NouveauLieu = nl.idlieu
            WHERE a.numAffect = ?
        """, (numAffect,))
        return cursor.fetchone()
    
    def get_employee_assignments(self, numEmp):
        """Get all assignments for a specific employee."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.*, 
                   al.design as ancien_lieu_design, al.province as ancien_province,
                   nl.design as nouveau_lieu_design, nl.province as nouveau_province
            FROM AFFECTER a
            JOIN LIEU al ON a.AncienLieu = al.idlieu
            JOIN LIEU nl ON a.NouveauLieu = nl.idlieu
            WHERE a.numEmp = ?
            ORDER BY a.dateAffect DESC, a.datePriseService DESC
        """, (numEmp,))
        return cursor.fetchall()
    
    def get_assignments_between_dates(self, start_date, end_date):
        """Get all assignments between two dates."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.*, 
                   e.civilite, e.nom, e.prenom, e.poste,
                   al.design as ancien_lieu_design, al.province as ancien_province,
                   nl.design as nouveau_lieu_design, nl.province as nouveau_province
            FROM AFFECTER a
            JOIN EMPLOYE e ON a.numEmp = e.numEmp
            JOIN LIEU al ON a.AncienLieu = al.idlieu
            JOIN LIEU nl ON a.NouveauLieu = nl.idlieu
            WHERE a.dateAffect BETWEEN ? AND ?
            ORDER BY a.dateAffect, a.datePriseService
        """, (start_date, end_date))
        return cursor.fetchall()
    
    def get_unassigned_employees(self):
        """Get all employees who don't have a current location assignment."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT e.* 
            FROM EMPLOYE e
            WHERE e.idlieu IS NULL
            ORDER BY e.nom, e.prenom
        """)
        return cursor.fetchall()
    
    def search_employees(self, search_term=None, location_id=None, position=None, province=None):
        """Search employees with various filters."""
        cursor = self.conn.cursor()
        
        query = """
            SELECT e.*, l.design as lieu_design, l.province 
            FROM EMPLOYE e
            LEFT JOIN LIEU l ON e.idlieu = l.idlieu
            WHERE 1=1
        """
        
        params = []
        
        if search_term:
            query += " AND (e.nom LIKE ? OR e.prenom LIKE ? OR e.mail LIKE ? OR e.numEmp LIKE ?)"
            search_param = f"%{search_term}%"
            params.extend([search_param, search_param, search_param, search_param])
        
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
        
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def get_employee_count(self):
        """Get the total number of employees."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM EMPLOYE")
        return cursor.fetchone()[0]
    
    def get_location_count(self):
        """Get the total number of locations."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM LIEU")
        return cursor.fetchone()[0]
    
    def get_assignment_count(self):
        """Get the total number of assignments."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM AFFECTER")
        return cursor.fetchone()[0]
    
    def get_monthly_assignment_count(self):
        """Get the number of assignments in the current month."""
        cursor = self.conn.cursor()
        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM AFFECTER 
            WHERE strftime('%Y-%m', dateAffect) = ?
        """, (current_month,))
        return cursor.fetchone()[0]
