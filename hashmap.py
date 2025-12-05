"""
FILE: hashmap.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

DESCRIPTION:
    Implements a Fixed-Size Hash Map from first principles.
    
    ARCHITECTURAL JUSTIFICATION (LO2):
    Native Rejection:
    This module explicitly rejects Python's built-in dictionary to demonstrate 
    the underlying mechanics of hashing and collision resolution.
    
    Separate Chaining:
    The system utilises Linked Lists (via the 'node' class) to handle 
    collisions within buckets. This strategy is chosen over Open Addressing 
    because Open Addressing suffers from 'Primary Clustering' as the load 
    factor approaches 1.0. In a hospital context, we cannot risk the database 
    'locking up' during a surge. Separate Chaining ensures graceful degradation 
    (search time becomes O(N/k)) rather than failure.
"""

from node import node 

class hashmap:
    """
    Implements an associative array (Key-Value Store).
    
    Collision Resolution Strategy: 
         Separate Chaining via Linked Lists.
         
    Time Complexity:
         Average Case: O(1) for Put/Get operations.
         Worst Case: O(N) (if all keys hash to the same bucket).
    """
    def __init__(self, capacity=10):
        """
        Initialises buckets for separate chaining.
        
        Args:
            capacity (int): The initial number of buckets.
        """
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        
        # Industry standard load factor for Separate Chaining.
        # When size > 0.7 * capacity, performance degrades, triggering resize.
        self.MAX_LOAD_FACTOR = 0.7 

    def _hash(self, key: str) -> int:
        """
        Computes index via ASCII summation modulo capacity.
        
        Formula: sum(ASCII) % capacity
        """
        hash_sum = 0
        for char in key:
            hash_sum += ord(char)
        return hash_sum % self.capacity

    def _resize(self):
        """
        Doubles the map capacity and rehashes all existing elements.
        Executed when the Load Factor is exceeded to maintain O(1) average access.
        
        Complexity: O(N) - Must touch every existing element.
        """
        print(f"--- [RESIZE] Capacity doubled from {self.capacity} to {self.capacity * 2} ---")
        
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0 # Size will be re-calculated during re-insertion

        # Iterate over the old structure and re-insert elements
        for head_node in old_buckets:
            current = head_node
            while current:
                key, value = current.get_value()
                # Re-inserting uses the new (larger) capacity
                self.put(key, value) 
                current = current.get_next_node()

    def put(self, key: str, value):
        """
        Inserts or updates a Key-Value pair.
        
        Complexity: O(1) Average.
        """
        # Check Load Factor and Trigger Resize if threshold is met
        if self.size / self.capacity >= self.MAX_LOAD_FACTOR:
            self._resize()

        index = self._hash(key)
        # Payload is stored as a tuple (key, value)
        new_node = node((key, value))
        
        # Case 1: Bucket is empty (No Collision)
        if self.buckets[index] is None:
            self.buckets[index] = new_node
            self.size += 1
            return

        # Case 2: Collision - Traverse the chain to update or append
        current = self.buckets[index]
        while current:
            stored_key, stored_val = current.get_value()
            
            # Update existing key
            if stored_key == key:
                current.value = (key, value) 
                return
            
            # End of chain reached
            if current.get_next_node() is None:
                break
            current = current.get_next_node()
        
        # Case 3: Key not found in chain, Append to end
        current.set_next_node(new_node)
        self.size += 1

    def get(self, key: str):
        """
        Retrieves value associated with key.
        
        Returns:
            The value associated with the key, or None if not found.
        """
        index = self._hash(key)
        current = self.buckets[index]
        
        # Traverse the linked list at this bucket
        while current:
            stored_key, stored_val = current.get_value()
            if stored_key == key:
                return stored_val
            current = current.get_next_node()
            
        return None