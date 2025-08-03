from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union
from datetime import date, datetime
import sqlite3

T = TypeVar('T', bound='BaseModel')

class BaseModel:
    """Base model class that provides common database operations."""
    
    # Table name should be overridden by subclasses
    TABLE_NAME = None
    
    # Primary key field name should be overridden by subclasses
    PRIMARY_KEY = 'id'
    
    # Field definitions should be overridden by subclasses
    # Format: {'field_name': 'sqlite_type'}
    FIELDS = {}
    
    def __init__(self, **kwargs):
        """Initialize the model with the given attributes."""
        for field in self.FIELDS:
            setattr(self, field, kwargs.get(field))
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create a model instance from a dictionary."""
        return cls(**{
            k: v for k, v in data.items() 
            if k in cls.FIELDS
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {
            field: getattr(self, field, None)
            for field in self.FIELDS
        }
    
    def save(self, db: 'Database') -> Tuple[bool, str]:
        """Save the model to the database.
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if getattr(self, self.PRIMARY_KEY, None) is None:
            return self._insert(db)
        return self._update(db)
    
    def _insert(self, db: 'Database') -> Tuple[bool, str]:
        """Insert a new record into the database."""
        fields = [f for f in self.FIELDS if f != self.PRIMARY_KEY]
        placeholders = ', '.join(['?'] * len(fields))
        field_names = ', '.join(fields)
        
        query = f"""
            INSERT INTO {self.TABLE_NAME} ({field_names})
            VALUES ({placeholders})
        """
        
        values = [getattr(self, field) for field in fields]
        
        try:
            cursor = db.conn.cursor()
            cursor.execute(query, values)
            
            # If there's an auto-incrementing primary key, get its value
            if cursor.lastrowid:
                setattr(self, self.PRIMARY_KEY, cursor.lastrowid)
            
            db.conn.commit()
            return True, f"{self.__class__.__name__} created successfully!"
        except sqlite3.IntegrityError as e:
            return False, f"Error creating {self.__class__.__name__.lower()}: {str(e)}"
    
    def _update(self, db: 'Database') -> Tuple[bool, str]:
        """Update an existing record in the database."""
        fields = [f for f in self.FIELDS if f != self.PRIMARY_KEY]
        set_clause = ', '.join([f"{field} = ?" for field in fields])
        
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET {set_clause}
            WHERE {self.PRIMARY_KEY} = ?
        """
        
        values = [getattr(self, field) for field in fields]
        values.append(getattr(self, self.PRIMARY_KEY))
        
        try:
            cursor = db.conn.cursor()
            cursor.execute(query, values)
            db.conn.commit()
            
            if cursor.rowcount == 0:
                return False, f"{self.__class__.__name__} not found!"
                
            return True, f"{self.__class__.__name__} updated successfully!"
        except Exception as e:
            return False, f"Error updating {self.__class__.__name__.lower()}: {str(e)}"
    
    @classmethod
    def delete(cls, db: 'Database', pk: Any) -> Tuple[bool, str]:
        """Delete a record from the database.
        
        Args:
            db: Database connection
            pk: Primary key value of the record to delete
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        query = f"""
            DELETE FROM {cls.TABLE_NAME}
            WHERE {cls.PRIMARY_KEY} = ?
        """
        
        try:
            cursor = db.conn.cursor()
            cursor.execute(query, (pk,))
            db.conn.commit()
            
            if cursor.rowcount == 0:
                return False, f"{cls.__name__} not found!"
                
            return True, f"{cls.__name__} deleted successfully!"
        except sqlite3.IntegrityError as e:
            return False, f"Cannot delete {cls.__name__.lower()}: Record is referenced by other tables."
        except Exception as e:
            return False, f"Error deleting {cls.__name__.lower()}: {str(e)}"
    
    @classmethod
    def get(cls, db: 'Database', pk: Any) -> Optional['BaseModel']:
        """Get a single record by primary key."""
        query = f"""
            SELECT * FROM {cls.TABLE_NAME}
            WHERE {cls.PRIMARY_KEY} = ?
        """
        
        cursor = db.conn.cursor()
        cursor.execute(query, (pk,))
        row = cursor.fetchone()
        
        if not row:
            return None
            
        return cls.from_row(row)
    
    @classmethod
    def get_all(cls, db: 'Database', order_by: str = None) -> List['BaseModel']:
        """Get all records from the table."""
        query = f"SELECT * FROM {cls.TABLE_NAME}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        cursor = db.conn.cursor()
        cursor.execute(query)
        
        return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def from_row(cls, row: tuple) -> 'BaseModel':
        """Create a model instance from a database row."""
        # Get column names from the cursor description
        columns = [col[0] for col in row.keys()] if hasattr(row, 'keys') else None
        
        if columns:
            # If row is a dictionary-like object (from cursor with row_factory=sqlite3.Row)
            data = dict(row)
        else:
            # If row is a tuple, use the order of FIELDS
            data = {}
            for i, field in enumerate(cls.FIELDS):
                if i < len(row):
                    data[field] = row[i]
        
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation of the model."""
        attrs = ', '.join([f"{k}={v!r}" for k, v in self.to_dict().items()])
        return f"{self.__class__.__name__}({attrs})"
