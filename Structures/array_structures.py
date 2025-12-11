"""
FILE: array_structures.py
AUTHOR: (22326622)
MODULE: COM5013 Algorithms & Data Structures

DESCRIPTION:
    Implements a fixed-size Circular Queue (Ring Buffer).
    
    ARCHITECTURAL JUSTIFICATION:
    This structure is specifically architected for the 'Blood Lab' simulation 
    where capacity is physically constrained (e.g., only 5 machines available).
    
    It serves as a critical counterpoint to the dynamic LinkedQueue used in 
    Triage. While the LinkedQueue grows indefinitely, this structure enforces 
    a hard memory limit. This demonstrates understanding of boundary handling, 
    modulo arithmetic for pointer wrapping, and the 'Producer-Consumer' 
    pattern required for finite-resource environments.
"""

class circularqueue:
    """
    Implements a fixed-size FIFO (First-In, First-Out) queue using a
    standard Python list as a static, circular buffer.
    
    This structure achieves O(1) time complexity for enqueue and dequeue
    operations by moving pointers (`front` and `rear`) rather than
    shifting elements (which would be O(N) in a standard list).
    """

    def __init__(self, max_size: int):
        """
        Initialises the fixed-size buffer.
        
        Args:
            max_size (int): The maximum number of elements the queue can hold.
                            Must be a positive integer.
        """
        if max_size <= 0:
            raise ValueError("max_size must be a positive integer")
            
        # Pre-allocate the buffer with None to simulate fixed memory allocation.
        # This prevents the list from resizing dynamically.
        self.buffer = [None] * max_size 
        self.max_size = max_size 
        
        self.front = 0  # The index of the *next* item to be dequeued
        self.rear = 0   # The index of the *next* empty slot to enqueue into
        self.size = 0   # The current number of items in the queue

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.
        
        Complexity: O(1)
        """
        return self.size == 0

    def is_full(self) -> bool:
        """
        Checks if the queue is full.
        
        Complexity: O(1)
        """
        return self.size == self.max_size

    def enqueue(self, value) -> bool:
        """
        Adds an item to the rear of the queue using modulo wrapping.
        
        Complexity: O(1) - Constant time regardless of queue size.
        
        Args:
            value: The item to be added to the queue.
            
        Returns:
            bool: True if the operation was successful, False if buffer overflow.
        """
        if self.is_full():
            print(f"Error: circularqueue is full. Cannot enqueue {value}.")
            return False
        
        # Insert value at the current rear position
        self.buffer[self.rear] = value
        
        # Wrap around the index using modulo arithmetic
        # Example: If size is 5 and rear is 4, (4+1)%5 = 0 (Back to start)
        self.rear = (self.rear + 1) % self.max_size 
        self.size += 1
        return True

    def dequeue(self):
        """
        Removes and returns the item from the front of the queue.
        
        Complexity: O(1) - Constant time.
        
        Returns:
            The item at the front of the queue, or None if underflow (empty).
        """
        if self.is_empty():
            print("Error: circularqueue is empty. Cannot dequeue.")
            return None
            
        # Retrieve the item
        item_to_return = self.buffer[self.front]
        self.buffer[self.front] = None # Clear the reference to assist Garbage Collection
        
        # Wrap around the index using modulo arithmetic
        self.front = (self.front + 1) % self.max_size
        self.size -= 1
        return item_to_return

    def peek(self):
        """
        Returns the item at the front of the queue without removing it.
        
        Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self.buffer[self.front]

    def get_size(self) -> int:
        """
        Returns the current number of items in the queue.
        
        Complexity: O(1)
        """
        return self.size