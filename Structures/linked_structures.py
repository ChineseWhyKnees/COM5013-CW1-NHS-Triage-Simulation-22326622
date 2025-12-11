"""
FILE: linked_structures.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

This module defines two fundamental linked data structures: a **stack** and
a **queue**. Both are implemented using a basic :class:`Structures.node.node` class
that stores a value and a pointer to the next node. Linked structures
serve as the building blocks for many parts of the triage simulation:

* The history log on each patient record uses a stack so that the most
  recent event can be accessed quickly.
* The triage and pharmacy lines use a queue so that patients are served in
  the order they arrive first-in, first-out (FIFO).

By implementing these structures manually rather than relying on Python's
list type we avoid hidden linear-time operations such as ``pop(0)`` and
learn how pointers can be manipulated directly to achieve constant time
inserts and removals. The code here is careful not to shift any
elements; instead it updates node references to move the head or tail.

Other modules in the simulation import these classes to store patients in
queues (for example, the pharmacy queue) and to keep track of actions in
the administrator audit log. Because the structures are simple and
self-contained, they can be reused in multiple contexts without
modification.
"""

from Structures.node import node # Import the custom Node primitive

class linkedstack:
    """
    A last-in, first-out (LIFO) stack implemented with linked nodes.

    Each time a value is pushed onto the stack a new node is created
    and inserted at the front. Popping removes the node at the front
    and returns its value. Because nodes are linked, no shifting of
    elements is required; pointer updates suffice. The stack keeps
    track of how many items it contains via a ``size`` attribute.

    This structure is used in the simulation for logging events, both
    within patient records (to record status history) and within the
    administrator interface (to record actions). It ensures that the
    most recent entry can always be retrieved immediately.
    """
    def __init__(self):
        """
        Create an empty stack.

        The ``top_item`` pointer starts as ``None`` indicating that the
        stack contains no nodes. The ``size`` counter is set to zero.
        """
        self.top_item = None
        self.size = 0

    def push(self, value):
        """
        Add a value to the top of the stack.

        A new :class:`Structures.node.node` is created to hold ``value``.
        Its ``next_node`` pointer is set to the current ``top_item`` so
        that it becomes the new first element. The ``top_item`` pointer
        and ``size`` counter are then updated to reflect the new state.
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
        Remove and return the most recently added value.

        If the stack is empty this method returns ``None``. Otherwise it
        retrieves the current ``top_item``, moves the ``top_item`` pointer
        to the next node in the chain and decrements ``size``. The value
        stored in the removed node is returned to the caller.
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
        Look at the value on the top of the stack without removing it.

        Returns:
            The value stored in the top node, or ``None`` if the stack is
            empty.
        """
        if self.is_empty():
            return None
        return self.top_item.get_value()

    def is_empty(self) -> bool:
        """
        Return ``True`` if the stack has no elements, ``False`` otherwise.
        """
        return self.size == 0

    def get_size(self) -> int:
        """
        Return the number of items currently stored in the stack.
        """
        return self.size


class linkedqueue:
    """
    A first-in, first-out (FIFO) queue implemented with linked nodes.

    Values are added at the tail of the queue and removed from the head.
    Because the queue maintains explicit pointers to both ends, enqueue
    and dequeue operations run in constant time. A ``size`` counter
    tracks how many nodes are present.

    This structure replaces the use of ``list.pop(0)`` which would be
    inefficient for large lists. It is used throughout the simulation to
    manage patients waiting for treatment (for example, the pharmacy
    queue). The semantics ensure that patients are served in the order
    they arrive.
    """
    def __init__(self):
        """
        Create an empty queue.

        Both ``head`` and ``tail`` pointers start as ``None``, indicating
        that there are no nodes in the chain. The ``size`` attribute is
        set to zero. As items are enqueued or dequeued the pointers and
        size counter are updated accordingly.
        """
        self.head = None # Pointer for Dequeue operations
        self.tail = None # Pointer for Enqueue operations
        self.size = 0

    def enqueue(self, value):
        """
        Add a value to the end of the queue.

        A new :class:`Structures.node.node` is created and attached to the
        current ``tail``. If the queue is empty the new node becomes both
        the ``head`` and ``tail``. Otherwise the ``next_node`` of the
        current tail is set to point to the new node and ``tail`` is
        updated. The ``size`` counter is incremented.
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
        Remove and return the oldest value in the queue.

        If the queue is empty this method returns ``None``. Otherwise it
        retrieves the value from the ``head`` node, moves ``head`` to the
        next node in the chain and decrements ``size``. If the queue
        becomes empty as a result, the ``tail`` pointer is also reset to
        ``None``. This operation runs in constant time.
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
        Return ``True`` if the queue contains no elements, ``False`` otherwise.
        """
        return self.size == 0
    
    def get_size(self) -> int: 
        """
        Return the number of items currently stored in the queue.
        
        Because the queue maintains a ``size`` attribute, this method
        simply returns that value without needing to traverse the chain.
        """
        return self.size