"""
FILE: linked_structures.py
AUTHOR: Brayden Louis Smith (22326622)
MODULE: COM5013 Algorithms & Data Structures

DESCRIPTION:
    Implements manual, pointer-based linear data structures to satisfy 
    the "First Principles" project constraint.
    
    1. LinkedQueue: A FIFO structure using Head/Tail pointers. 
       Selected to replace Python's 'list.pop(0)' to guarantee O(1) 
       time complexity during high-volume triage.
       
    2. LinkedStack: A LIFO structure.
       Used specifically for the PatientRecord 'history_log' (Audit Trail)
       to ensure that the most recent clinical event is always accessible 
       at the head of the list in O(1) time.

DEPENDENCIES:
    node.py (The atomic wrapper)
"""

from node import node  # Import the custom Node primitive

class linkedstack:
    """
    Implements a Last-In, First-Out (LIFO) stack using a singly linked list.
    
    ARCHITECTURAL JUSTIFICATION:
    While Python lists can function as stacks via append/pop, a Linked Stack
    is implemented here to demonstrate understanding of pointer manipulation
    at the head of a list (Push/Pop at index 0 without shifting).
    
    Time Complexity:
        Push: O(1) - Constant time pointer update.
        Pop: O(1) - Constant time pointer update.
        Peek: O(1) - Constant time access.
    """
    def __init__(self):
        """
        Initialises stack state with null pointers.
        """
        self.top_item = None
        self.size = 0

    def push(self, value):
        """
        Inserts an element at the top of the stack.
        
        Logic:
            1. Allocate new Node.
            2. Link new Node -> Current Top.
            3. Reassign Top -> New Node.
        """
        # 1. Allocation
        new_node = node(value)
        
        # 2. Linkage
        new_node.set_next_node(self.top_item)
        
        # 3. Pointer Update
        self.top_item = new_node
        self.size += 1

    def pop(self):
        """
        Removes and returns the element at the top of the stack.
        
        Returns:
            The value of the popped element, or None if empty.
        """
        if self.is_empty():
            return None
        
        # 1. Identify target node
        item_to_remove = self.top_item
        
        # 2. Shift pointer to the next node in sequence
        self.top_item = item_to_remove.get_next_node()
        self.size -= 1
        
        # 3. Return payload
        return item_to_remove.get_value()

    def peek(self):
        """
        Returns the payload of the top element without structural modification.
        """
        if self.is_empty():
            return None
        return self.top_item.get_value()

    def is_empty(self) -> bool:
        """Boolean check for empty state."""
        return self.size == 0

    def get_size(self) -> int:
        """Returns current node count."""
        return self.size


class linkedqueue:
    """
    Implements a First-In, First-Out (FIFO) queue using a singly linked list.
    
    ARCHITECTURAL JUSTIFICATION (LO2):
    This structure is the direct result of the architectural rescope.
    Unlike 'list.pop(0)' which shifts N elements (O(N)), this implementation
    simply advances the 'head' pointer (O(1)), satisfying the NHS 
    latency requirement for deterministic patient discharge.
    """
    def __init__(self):
        """
        Initialises queue with null head and tail pointers.
        """
        self.head = None  # Pointer for Dequeue operations
        self.tail = None  # Pointer for Enqueue operations
        self.size = 0

    def enqueue(self, value):
        """
        Appends an element to the tail of the queue.
        Complexity: O(1).
        """
        new_node = node(value)
        
        if self.is_empty():
            # If empty, the new node serves as both head and tail
            self.head = new_node
            self.tail = new_node
        else:
            # 1. Link current tail to new node
            self.tail.set_next_node(new_node)
            # 2. Update tail pointer to the new node
            self.tail = new_node
            
        self.size += 1

    def dequeue(self):
        """
        Removes and returns the element at the head of the queue.
        
        Complexity: O(1) Strictly Constant Time.
        This is the critical path operation for the Triage System.
        """
        if self.is_empty():
            return None
        
        # 1. Retrieve payload
        value_to_return = self.head.get_value()
        
        # 2. Advance head pointer to the next node
        self.head = self.head.get_next_node()
        self.size -= 1
        
        # 3. Boundary condition: If queue is now empty, nullify tail
        if self.size == 0:
            self.tail = None
            
        return value_to_return

    def is_empty(self) -> bool:
        """
        Checks if queue is empty.
        """
        return self.size == 0
    
    def get_size(self) -> int: 
        """
        Returns the current number of items in the queue. O(1).
        """
        return self.size