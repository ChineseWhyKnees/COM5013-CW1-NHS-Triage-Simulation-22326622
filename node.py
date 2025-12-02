"""
FILE: node.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

DESCRIPTION:
    Defines the fundamental atomic unit for all non-linear data structures 
    in the NHS Triage System simulation.
    
    ARCHITECTURAL JUSTIFICATION (FIRST PRINCIPLES):
    In adherence to the project's constraint of rejecting high-level abstractions, 
    this class manually manages memory references via the 'next_node' pointer. 
    
    This approach is architected specifically to circumvent the O(N) memory 
    shifting penalties inherent in Python's standard dynamic arrays (lists). 
    By using discrete Nodes, we enable O(1) insertion and deletion at the 
    head of a queue, a critical requirement for safety-critical latency 
    within the triage environment.
"""

class node:
    """
    Represents a single node in a linked data structure.
    
    This class functions as the foundational building block for:
    1. LinkedStack (LIFO) - Used for Patient Audit Trails.
    2. LinkedQueue (FIFO) - Used for the Triage Line.
    3. HashMap Buckets - Used for Separate Chaining collision resolution.
    
    It couples a data element (value) with a reference (pointer) to the
    next node in the chain, effectively decoupling storage from contiguous memory.
    """

    def __init__(self, value, next_node=None):
        """
        Initialises a new Node instance.

        Args:
            value: The data payload (e.g., PatientRecord object) to be 
                   stored within this memory block.
            next_node (node, optional): The reference to the subsequent node
                   in the linked chain. Defaults to None (Tail).
        """
        self.value = value
        
        # The pointer to the subsequent node in the chain.
        # Explicit management of this attribute allows for O(1) graph traversal.
        self.next_node = next_node

    def get_value(self):
        """
        Retrieves the data payload stored in this node.
        
        Complexity: O(1) - Direct memory access.
        
        Returns:
            The value stored in the node.
        """
        return self.value

    def get_next_node(self):
        """
        Retrieves the reference to the next node in the chain.
        
        Used by LinkedQueue and LinkedStack to traverse the structure 
        without indexing/offsets.
        
        Returns:
            node: The next Node object, or None if this is the tail.
        """
        return self.next_node

    def set_next_node(self, next_node):
        """
        Updates the reference to the next node in the chain.
        
        CRITICAL PERFORMANCE MECHANIC:
        Changing this reference is a strictly O(1) operation. 
        Unlike inserting into an array, which requires shifting N elements,
        this method simply updates a single memory address.

        Args:
            next_node (node): The Node to set as the next node.
        """
        self.next_node = next_node