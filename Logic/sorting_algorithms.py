"""
FILE: sorting_algorithms.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

This module provides a *stable* merge sort implementation used by the
triage simulation to order patients by priority. A stable sort ensures
that when two items compare as equal (for example, two patients with the
same priority), they remain in the same relative order as they were
before sorting. This property is important in the simulation so that
patients who arrive earlier are treated before those who arrive later
when their priorities match.

The functions defined here operate on generic lists and rely only on the
``<`` operator to compare elements. In particular, they expect that
``patientrecord`` objects implement ``__lt__`` appropriately (see
:mod:`Logic.patient_record`) so that patients are sorted first by urgency
and then by NHS number.

Under the hood merge sort uses a divide-and-conquer strategy: it splits
the input list into two halves, recursively sorts each half, and then
merges the sorted halves back together. This process runs in O(n log n)
time and does not modify the original list in place.
"""

from typing import List, TypeVar

# Generic type variable to indicate this function handles sortable objects
T = TypeVar('T')

def merge_sort(items: List[T]) -> List[T]:
    """
    Sort a list of comparable items using merge sort.

    Merge sort is a recursive algorithm that divides the input list into
    smaller pieces, sorts each piece, and then combines the pieces into a
    single sorted list. Because it returns a new list rather than
    rearranging the original, the original ``items`` list is left
    untouched.

    Parameters:
        items: a list of objects that can be compared using the ``<``
            operator. For patient records this means implementing a
            ``__lt__`` method that defines the ordering criteria.

    Returns:
        A new list containing the elements of ``items`` in ascending order.
    """
    # Base Case: A list of 0 or 1 elements is intrinsically sorted.
    if len(items) <= 1:
        return items
    
    # 1. DIVIDE
    mid_point = len(items) // 2
    left_segment = items[:mid_point]
    right_segment = items[mid_point:]
    
    # 2. CONQUER
    sorted_left = merge_sort(left_segment)
    sorted_right = merge_sort(right_segment)
    
    # 3. MERGE
    return _merge(sorted_left, sorted_right)

def _merge(left: List[T], right: List[T]) -> List[T]:
    """
    Merge two sorted sublists into a single sorted list.

    This helper function is called by :func:`merge_sort`. It takes two
    lists that are already sorted and interleaves their elements into a
    new list in order. To preserve *stability*, if an element of
    ``right`` is strictly less than an element of ``left`` then it comes
    first; otherwise the element from ``left`` is taken. This means that
    when two items compare as equal the one from ``left`` (which came
    earlier in the original list) will appear first in the result.

    Parameters:
        left: a list of sorted items.
        right: another list of sorted items.

    Returns:
        A new list containing all elements from ``left`` and ``right`` in
        sorted order.
    """
    merged_result = []
    left_index = 0
    right_index = 0
    
    while left_index < len(left) and right_index < len(right):
        
        # --- STABILITY LOGIC ---
        # Check if Right is STRICTLY smaller (higher priority).
        # If Right < Left: Right goes first.
        # If Right is NOT < Left (meaning Left <= Right): Left goes first.
        # This preserves arrival order for ties.
        if right[right_index] < left[left_index]:
            merged_result.append(right[right_index])
            right_index += 1
        else:
            merged_result.append(left[left_index])
            left_index += 1
            
    # Append any remaining elements
    if left_index < len(left):
        merged_result.extend(left[left_index:])
        
    if right_index < len(right):
        merged_result.extend(right[right_index:])
        
    return merged_result