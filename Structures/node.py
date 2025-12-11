"""
FILE: node.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

This module defines the simplest building block used by the custom linked
structures in the triage simulation. A **node** stores a value (such as
a patient record or an action string) and a reference to another node. By
linking nodes together in chains we can create stacks, queues and other
data structures without relying on Python's built-in list type. The
purpose of doing this from scratch is to make the cost of operations
explicit: adding or removing a node at the beginning of a chain takes
constant time because only a pointer needs to be updated.

The :class:`node` class itself is very small; it exposes methods to get
and set the stored value and the link to the next node. Other modules
build on top of it to assemble more complex behaviour.
"""

class node:
    """
    A minimal object for linking values together.

    Each node holds two things: a ``value`` and a reference to the next
    node in a chain. When many nodes are linked in sequence they form
    basic data structures such as stacks, queues or chains of entries in
    a hash map. Separating values into individual nodes allows us to
    insert and remove items at the front of a chain without moving any
    other elements in memory.
    """

    def __init__(self, value, next_node=None):
        """
        Create a new node.

        Parameters:
            value: the data to store in this node. It can be of any type,
                such as a patient record or a string describing an event.
            next_node: an optional reference to another node. When linking
                nodes together this parameter points to the node that
                follows this one. By default it is ``None`` to signal
                that this node is the end of a chain.
        """
        self.value = value
        
        # The pointer to the subsequent node in the chain.
        # Explicit management of this attribute allows for O(1) graph traversal.
        self.next_node = next_node

    def get_value(self):
        """
        Return the value stored in this node.

        This is a simple accessor that returns whatever was provided when
        the node was created or later modified via :meth:`set_next_node`.

        Returns:
            The stored value.
        """
        return self.value

    def get_next_node(self):
        """
        Return the next node in the chain.

        Other data structures use this method to move from one node to the
        next without needing to know the internal representation of the
        chain.

        Returns:
            The node referenced by ``next_node``, or ``None`` if this is
            the last node.
        """
        return self.next_node

    def set_next_node(self, next_node):
        """
        Set the link to the next node in the chain.

        Updating the ``next_node`` pointer does not move any data; it
        simply changes where this node points. This is why linked
        structures can insert or remove items in constant time.

        Parameters:
            next_node: the node that should follow this one. Use ``None``
            to mark this node as the end of a chain.
        """
        self.next_node = next_node