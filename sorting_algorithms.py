"""
FILE: sorting_algorithms.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

DESCRIPTION:
    Implements the sorting logic required to prioritise the patient queue.
    
    ARCHITECTURAL JUSTIFICATION (LO2):
    A custom recursive Merge Sort was selected over Quick Sort or Python's 
    Timsort for specific clinical reasons:
    
    Stability:
    Merge Sort is 'Stable'. It preserves the relative order of records with 
    equal keys. In a triage context, if two patients have the same Priority, 
    the one who arrived first (lower NHS number) must be treated first. 
    Unstable sorts (like Quick Sort) fail this ethical requirement.
       
    Predictability:
    Merge Sort offers a consistent O(N log N) worst-case time complexity, 
    unlike Quick Sort which can degrade to O(N^2) on already-sorted data.
       
    Recursion:
    This implementation exposes the Divide-and-Conquer mechanics explicitly, 
    fulfilling the 'First Principles' constraint.

TECHNICAL NOTE (IMPORTS):
    This module imports 'List' and 'TypeVar' from the 'typing' library.
    These are strict 'Infrastructure' imports used solely for static analysis 
    and code quality (LO3). They do not provide any algorithmic logic or 
    runtime shortcuts, preserving the First Principles integrity.
"""

from typing import List, TypeVar

# Generic type variable to indicate this function handles sortable objects
T = TypeVar('T')

def merge_sort(items: List[T]) -> List[T]:
    """
    Implements the Merge Sort algorithm using a recursive Divide and Conquer strategy.
    
    Time Complexity: O(N log N) (Best/Average/Worst).
    Space Complexity: O(N) auxiliary.
         
    Args:
        items (List[T]): A list of objects implementing the __lt__ comparison operator.
        
    Returns:
        List[T]: A new list containing the sorted elements.
    """
    # Base Case: A list of 0 or 1 elements is intrinsically sorted.
    if len(items) <= 1:
        return items
    
    # 1. DIVIDE: Calculate the midpoint to split the dataset.
    mid_point = len(items) // 2
    
    # Slice the list into two halves.
    left_segment = items[:mid_point]
    right_segment = items[mid_point:]
    
    # 2. CONQUER: Recursively sort both sub-segments.
    sorted_left = merge_sort(left_segment)
    sorted_right = merge_sort(right_segment)
    
    # 3. MERGE: Combine the two sorted sub-segments.
    return _merge(sorted_left, sorted_right)

def _merge(left: List[T], right: List[T]) -> List[T]:
    """
    Helper function to merge two sorted lists into a single sorted sequence.
    
    Logic:
        Maintains pointers (indices) for both lists.
        Compares the head of both lists using the object's comparison logic.
        Appends the smaller (or equal) element to the result list.
        
    Complexity: O(N) where N is the total number of elements in both lists.
    """
    merged_result = []
    left_index = 0
    right_index = 0
    
    while left_index < len(left) and right_index < len(right):
        
  # --- STABILITY MECHANISM ---
        # To maintain sort stability (choosing Left first when items are equal),
        # we check if Right is strictly smaller than Left.
        # If right < left: Right is smaller, append Right.
        # Else (left <= right): Left is smaller or equal, append Left.
        if left[left_index] < right[right_index]:
            merged_result.append(left[left_index])
            left_index += 1
        else:
            merged_result.append(right[right_index])
            right_index += 1
            
    # Append any remaining elements from the left list
    if left_index < len(left):
        merged_result.extend(left[left_index:])
        
    # Append any remaining elements from the right list
    if right_index < len(right):
        merged_result.extend(right[right_index:])
        
    return merged_result