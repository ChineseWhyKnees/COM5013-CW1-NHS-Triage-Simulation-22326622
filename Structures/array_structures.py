"""
FILE: array_structures.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

This module implements a **circular queue**, also known as a ring buffer,
which holds a fixed number of items and then wraps around to the beginning.
In the context of the triage simulation the circular queue is used to model
the blood laboratory where only a limited number of samples can be processed
at any one time. When the buffer is full no more patients can be added to
the lab until someone is removed, mirroring a real-world bottleneck.

A circular queue differs from a dynamic queue in that it never grows beyond
its initial capacity. It uses two pointers—``front`` and ``rear``—to keep
track of where to remove and insert items. As each pointer reaches the
end of the underlying list it wraps around to the beginning. This
wrap-around behaviour is implemented using modular arithmetic. The result
is that both enqueueing and dequeueing can be performed in constant time
without shifting any elements.

This data structure is consumed by the main program when adding patients to
and removing them from the lab buffer. Other modules interact with it
through its public methods and do not need to know how the wrapping works.
"""

class circularqueue:
    """
    A first-in, first-out (FIFO) queue with a fixed maximum size.

    Internally this queue uses a Python list of a given length as a
    container. Two integer indices, ``front`` and ``rear``, mark the
    positions of the next element to be removed and the next empty slot to
    fill. When either index reaches the end of the list it loops back to
    zero. Because the list is pre-allocated and only these two pointers
    change, adding or removing items does not require shifting any values
    within the list and therefore takes constant time.
    """

    def __init__(self, max_size: int):
        """
        Create a new circular queue with a fixed capacity.

        Parameters:
            max_size: the number of slots to allocate in the underlying
                buffer. This must be a positive integer. Once created the
                queue will never hold more than ``max_size`` items.

        The internal list is filled with ``None`` values to reserve memory.
        The ``front`` index starts at 0 (the first slot) and ``rear``
        starts at 0 (the next free slot). The ``size`` attribute keeps
        track of how many items are actually in the queue.
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
        Check whether the queue has no items.

        Returns:
            ``True`` if there are no elements in the buffer, ``False``
            otherwise.
        """
        return self.size == 0

    def is_full(self) -> bool:
        """
        Check whether the queue is at maximum capacity.

        Returns:
            ``True`` if ``size`` equals ``max_size``, meaning no more
            items can be enqueued, ``False`` otherwise.
        """
        return self.size == self.max_size

    def enqueue(self, value) -> bool:
        """
        Add a value to the end of the queue.

        This method stores ``value`` at the current ``rear`` position and
        then advances ``rear`` to the next slot, wrapping around to zero
        when necessary. If the buffer is full the operation fails and
        ``False`` is returned; otherwise ``True`` is returned after the
        item has been added.

        Parameters:
            value: the object to place into the queue. It can be of any
                type—commonly a :class:`Logic.patient_record.patientrecord`.

        Returns:
            ``True`` if the value was enqueued, or ``False`` if the queue
            was already full.
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
        Remove and return the oldest item in the queue.

        The element at index ``front`` is returned and that slot is set to
        ``None`` to aid garbage collection. The ``front`` index is then
        advanced one position, wrapping around to the start of the buffer
        when necessary. If the queue is empty a message is printed and
        ``None`` is returned.

        Returns:
            The value removed from the queue, or ``None`` if the queue
            contained no items.
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
        Inspect the value at the front of the queue without removing it.

        Returns:
            The element that would be returned by :meth:`dequeue`, or
            ``None`` if the queue is empty.
        """
        if self.is_empty():
            return None
        return self.buffer[self.front]

    def get_size(self) -> int:
        """
        Return the number of elements currently stored in the queue.

        This is a constant-time operation because the queue maintains a
        ``size`` attribute that is updated whenever items are enqueued or
        dequeued.
        """
        return self.size