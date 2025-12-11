"""
FILE: patient_record.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

DESCRIPTION:
    Defines the immutable data model for patient entities in the simulation.
    
    ARCHITECTURAL HIGHLIGHTS (FIRST PRINCIPLES):
    1. Immutability: Critical fields (NHS Number, DOB) are read-only properties 
       to ensure data integrity in a clinical safety context (LO2).
    2. Audit Trail: Each record encapsulates its own 'LinkedStack' to log 
       history (LIFO), enforcing the principle of Encapsulation.
    3. Comparability: Overrides __lt__ to enable the Merge Sort engine 
       to prioritise patients by medical urgency.

TECHNICAL POINT:
    Utilises 'TYPE_CHECKING' and 'annotations' to resolve circular dependencies
    between the Record (Logic) and the Stack (Structure) without breaking 
    the Python runtime environment.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

# Forward declaration to prevent Circular Import Error at runtime.
# This allows the Type Checker to see 'linkedstack' before the module is fully loaded.
if TYPE_CHECKING:
    from Structures.linked_structures import linkedstack

class patientrecord:
    """
    The primary data transfer object (DTO) for the triage system.
    
    This class enforces data integrity by making critical identifiers
    (nhs_number, dob) read-only after creation via @property decorators.
    It acts as the 'Payload' for the Node primitive.
    """
    
    def __init__(self, nhs_number: str, dob: str, first_name: str, last_name: str, priority: int, blood_type: str):
        """
        Initializes a new, immutable PatientRecord.
        
        Args:
            nhs_number (str): The unique identifier. Used as the Hash Key.
            dob (str): Date of Birth.
            first_name (str): Forename.
            last_name (str): Surname.
            priority (int): Medical urgency (1-5). Used as the Sort Key.
            blood_type (str): Blood Group.
        """
        # Local import to strictly adhere to dependency hierarchy.
        # Importing 'linkedstack' here avoids a global circular dependency loop 
        # with linked_structures.py, which imports 'node', which might infer 'patientrecord'.
        from linked_structures import linkedstack
        
        # Private attributes to enforce encapsulation
        self._nhs_number = nhs_number
        self._dob = dob
        self._first_name = first_name
        self._last_name = last_name
        self._priority = priority
        self._blood_type = blood_type
        
        # The LIFO Audit Log.
        # Justification: A Stack is used because the most recent clinical event 
        # is the most relevant for triage decisions.
        self.history_log: "linkedstack" = linkedstack()
        self.history_log.push(f"Patient record created with priority {priority}.")

    # --- Immutable Property Accessors (O(1)) ---
    # These prevent accidental modification of patient identity data.

    @property
    def nhs_number(self) -> str:
        """(str): Returns the patient's immutable NHS number. O(1)"""
        return self._nhs_number

    @property
    def dob(self) -> str:
        """(str): Returns the patient's immutable Date of Birth. O(1)"""
        return self._dob

    @property
    def first_name(self) -> str:
        """(str): Returns the patient's first name. O(1)"""
        return self._first_name

    @property
    def last_name(self) -> str:
        """(str): Returns the patient's last name. O(1)"""
        return self._last_name

    @property
    def priority(self) -> int:
        """(int): Returns the patient's current medical priority. O(1)"""
        return self._priority

    @priority.setter
    def priority(self, new_priority: int):
        """
        Controlled mutator for priority. 
        This is the only mutable critical field, reflecting dynamic clinical changes.
        Updates are automatically logged to the internal history stack.
        
        Args:
            new_priority (int): New priority level (1-5).
        """
        if not isinstance(new_priority, int) or not 1 <= new_priority <= 5:
            print(f"Error: Priority must be an integer between 1 and 5.")
            return
            
        self._priority = new_priority
        self.history_log.push(f"Priority updated to {new_priority}.")
        
    @property
    def blood_type(self) -> str:
        """(str): Returns the patient's immutable blood type. O(1)"""
        return self._blood_type
        
    def get_current_status(self) -> str:
        """
        Retrieves the latest status via O(1) Stack Peek.
        
        Returns:
            str: The most recent status message.
        """
        status = self.history_log.peek()
        return status if status is not None else "No status."

    def update_status(self, status_message: str):
        """
        Appends event to history log via O(1) Stack Push.
        
        Args:
            status_message (str): Description of the event.
        """
        self.history_log.push(status_message)

    def __lt__(self, other):
        """
        Defines 'Less Than' (<) logic for sorting algorithms.
        
        This method is the interface consumed by 'sorting_algorithms.py'.
        
        Logic:
            1. Primary Key: Medical Priority (1 is higher urgency than 5).
            2. Secondary Key: NHS Number (Tie-breaker).
               This ensures Stability: Identical priorities preserve arrival order 
               if the NHS number is sequential.
        """
        if not isinstance(other, patientrecord):
            return NotImplemented
        # 1. Primary Key: Medical Priority (Lower P = Higher Urgency)
        if self._priority != other._priority:
            return self._priority < other._priority
            
        # 2. Secondary Key: NHS Number (Arrival Order)
        # FIX: Cast to int() so "10" is correctly treated as larger than "2".
        return int(self._nhs_number) < int(other._nhs_number)

    def __repr__(self) -> str:
        """Provides a string representation for debugging and logging."""

        return f"[PatientRecord: {self._nhs_number} | {self._last_name}, {self._first_name} | P:{self._priority} | BT:{self._blood_type}]"
