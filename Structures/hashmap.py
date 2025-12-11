"""
FILE: hashmap.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

This module implements a simple **hash map**, a data structure that stores
key-value pairs and allows values to be looked up quickly by their keys.
Although Python provides its own dictionary type, this implementation
recreates the basics from the ground up to make the mechanics explicit.

Keys are strings (such as patient NHS numbers) and values can be any
object (commonly :class:`Logic.patient_record.patientrecord` instances). To
decide where to place a key-value pair in the underlying array, the
hash map computes a small integer called a *hash*. If multiple keys
produce the same hash value, they are stored together in a short linked
list (this technique is known as **separate chaining**). This approach
ensures that the map continues to function correctly even when the number
of stored elements grows beyond the number of available buckets.

The map automatically doubles its capacity when the *load factor* (the
ratio of stored elements to buckets) exceeds a threshold. Resizing the
buckets array and re-inserting the existing elements keeps operations like
insertion and lookup efficient on average.

This data structure underpins the patient database in the main program,
allowing records to be added and retrieved using their NHS numbers.
"""

from Structures.node import node 

class hashmap:
    """
    A minimal associative array for storing key-value pairs.

    This class provides the familiar operations of inserting (`put`) and
    retrieving (`get`) items by key. Internally it uses a fixed-length
    list of buckets to spread keys out. Each bucket holds a chain of
    :class:`Structures.node.node` objects that store the key and its
    associated value. When many keys map to the same bucket they are
    appended to the chain, which may degrade performance but will never
    cause a failure. When the number of stored items becomes too large
    relative to the number of buckets the map is *resized* (the number of
    buckets is doubled and all existing items are rehashed).

    The time complexity for inserting and retrieving items is generally
    constant (O(1)) on average, although it can become linear (O(n)) in the
    worst case when many keys collide in the same bucket.
    """
    def __init__(self, capacity=10):
        """
        Create a new hash map with a specified initial capacity.

        Parameters:
            capacity: the number of buckets to allocate. Each bucket is
                initially empty. Choosing a power of two (e.g. 10, 20, 40)
                simplifies some resizing strategies, but any positive
                integer will work.

        The map starts empty (`size` is zero) and uses a default maximum
        load factor of 0.7. When the ratio of `size` to `capacity`
        reaches this threshold the map will automatically resize.
        """
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        
        # Industry standard load factor for Separate Chaining.
        # When size > 0.7 * capacity, performance degrades, triggering resize.
        self.MAX_LOAD_FACTOR = 0.7 

    def _hash(self, key: str) -> int:
        """
        Compute a bucket index for a given string key.

        A very simple hash function sums the numeric (ASCII) codes of the
        characters in the key and then takes the remainder when dividing by
        the current capacity. The result is guaranteed to be a valid
        index into the `buckets` list.

        Parameters:
            key: the string to hash.

        Returns:
            An integer between 0 and ``capacity - 1``.
        """
        hash_sum = 0
        for char in key:
            hash_sum += ord(char)
        return hash_sum % self.capacity

    def _resize(self):
        """
        Double the number of buckets and re-insert all existing items.

        When the load factor limit is reached this method creates a new
        buckets list twice the size of the current one and then iterates
        over every existing key-value pair, placing each into its new
        bucket based on the resized capacity. Because each item must be
        touched this operation runs in linear time with respect to the
        number of stored items. After resizing the map's performance will
        improve because the average chain length has been reduced.
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
        Insert a new key-value pair or update an existing one.

        If the map's current load factor exceeds the maximum allowed this
        method calls :meth:`_resize` before inserting the new item. It
        computes the bucket index for the key using :meth:`_hash`. If no
        chain exists at that index a new node is created and placed there;
        otherwise the method walks down the chain:

        * If an existing node has the same key, its value is replaced with
          the new value.
        * If the end of the chain is reached and no matching key is found,
          a new node is appended to the chain.

        Parameters:
            key: a string used to locate the associated value later.
            value: the object to store.
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
        Retrieve the value associated with a given key.

        The bucket index for the key is computed using :meth:`_hash`, then
        the chain at that bucket is walked to find a node whose stored key
        matches the provided key. If such a node is found its value is
        returned; otherwise ``None`` is returned.

        Parameters:
            key: the string identifying the item to look up.

        Returns:
            The value stored with this key, or ``None`` if the key is not
            present in the map.
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
    