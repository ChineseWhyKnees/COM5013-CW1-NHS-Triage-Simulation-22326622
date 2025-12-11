# NHS Triage System Simulation

Author: 22326622
Module: COM5013 Algorithms & Data Structures
------------------------------------------------------------
## Project Overview

This application simulates a busy NHS Accident & Emergency triage desk.  It was
written from the ground up to expose the inner workings of common data
structures rather than leaning on Python's convenience functions.  Patients
arrive with a level of urgency, move through triage, pharmacy and laboratory
queues, and are eventually discharged.  Along the way the system must
prioritise the most serious cases while still treating everyone fairly.

### First Principles

In order to practice fundamental algorithms and data structures, I avoided
using Python’s built‑in queue, hash map, sorting and randomness libraries.
Instead I wrote my own versions for this project:

* list.pop(0) (dynamic array queue) → **manual linked queue** with constant‑time dequeue.
* dict (built‑in hash table) → **custom hash map** with separate chaining for collisions.
* list.sort() (Timsort) → **stable merge sort** to preserve arrival order on ties.
* random (Mersenne Twister) → **simple linear congruential generator** for reproducible pseudo‑random data.

------------------------------------------------------------

## Technical Architecture

The code is organised into two packages: **Logic** contains the algorithms and
business rules, and **Structures** contains the data storage primitives.

### Data Structures (Structures)

* **LinkedQueue** (in `linked_structures.py`) – A first‑in, first‑out queue built
  from linked nodes.  It avoids the O(N) penalty of shifting items in a list by
  simply updating head and tail pointers.  This queue is used for the triage and
  pharmacy lines.

* **LinkedStack** (in `linked_structures.py`) – A last‑in, first‑out stack for
  logging events.  Each patient record has its own stack of status messages, and
  an administrator audit log uses another stack.

* **HashMap** (in `hashmap.py`) – A simple key–value store using separate
  chaining to handle collisions.  Patient records are stored here keyed by NHS
  number.  When the map becomes too full it resizes itself to maintain near
  constant lookup time.

* **CircularQueue** (in `array_structures.py`) – A fixed‑size ring buffer used
  to represent the limited capacity of the lab.  It wraps around when reaching
  the end and refuses new items when full.

### Algorithmic Logic (Logic)

* **patient_generator.py** – Implements a lightweight linear congruential generator
  to pick random names, dates of birth, ailments, symptoms, medications and
  blood types.  Because the generator holds only a single integer, the
  sequence can be reproduced exactly by using the same seed.

* **patient_factory.py** – Wraps together the steps of allocating a unique NHS
  number, assigning a random priority and demographics, and creating a new
  patient record.  It is the single place where patients are born into the system.

* **patient_record.py** – Defines an immutable container for patient details plus a
  history log.  Records can be compared by priority (and NHS number as a tie‑breaker)
  so they can be sorted.

* **sorting_algorithms.py** – Provides a stable merge sort implementation used
  to order patients by urgency while preserving arrival order on ties.

* **main.py** – Brings all of the above components together in an interactive
  command‑line interface.  It manages queues, processes patients through stages,
  and includes a diagnostic suite to measure performance.

------------------------------------------------------------

## File Structure

The repository has a clear separation between data storage and business logic.
Each file plays a specific role in the simulation:

```
/NHS-Triage-System
|
├── main.py                   # Entry point: command‑line interface and diagnostic tools
├── Readme.txt                # This document
|
├── Structures/               # Custom memory management
|   ├── __init__.py
|   ├── node.py               # Atomic unit: a value with a pointer to the next node
|   ├── linked_structures.py  # LinkedQueue and LinkedStack implementations
|   ├── array_structures.py   # CircularQueue for fixed‑size buffers
|   └── hashmap.py            # HashMap with separate chaining
|
└── Logic/                    # Business rules and algorithms
    ├── __init__.py
    ├── patient_record.py     # Immutable patient details and history log
    ├── patient_generator.py  # Deterministic pseudo‑random data generator
    ├── patient_factory.py    # Creates complete patient records
    └── sorting_algorithms.py # Stable merge sort implementation
```

------------------------------------------------------------

## Usage Instructions

### Prerequisites

* No external libraries are required; everything uses the standard library.

### Running the Simulation

From the project root directory, execute:

```
python main.py
```

You will be prompted for credentials.  Use:

* **Username:** `SystemAdmin`
* **Password:** `22326622`

After logging in the program seeds the hospital with a number of patients,
indexes them in the database and sorts them by priority.  A menu then allows
you to search for patients, view queues, process patients through the pharmacy
and lab, and discharge and admit new patients.  Choosing **option 4** from the
menu runs a built‑in diagnostics suite that times various operations and prints
the results to the screen.

## Simulation Options

When you reach the main menu you'll see a numbered list of operations.  Each
one maps to a part of the underlying code:

1. **Patient Search (NHS Number) & Hand‑off** – Enter a patient's NHS number to
   retrieve their record from the hash map.  The system logs your search
   action in the administrator stack and, if the patient is found, displays
   their details.  You can then choose to send them to the pharmacy queue
   (linked queue), send them to the blood lab buffer (circular queue) or
   view their history log (linked stack).  Sending a patient adds a status
   message to their personal history and enqueues them into the appropriate
   structure.  Viewing the history uses a peek on the patient's stack so
   nothing is removed.

2. **View Recent Admissions (Sorted by Priority)** – Shows the top five
   patients from the master list, which is always kept sorted by the stable
   merge sort.  The list reflects the highest urgency cases first and
   preserves arrival order for patients with the same priority.

3. **System Statistics & Queue Status (Micro)** – Displays current counts of
   stored patients, how many are waiting in the pharmacy queue and lab
   buffer, and shows the most recent administrator action using a peek on
   the admin stack.  You can choose to process the queues, which dequeues
   one patient from each if available and updates their status (e.g. “Drugs
   Dispensed” or “Lab Results Analysed”).

4. **Run System Diagnostics (Stress Test)** – Launches the built‑in
   ``run_diagnostics`` function.  This runs a series of performance tests
   including sorting lists of increasing size, comparing the linked queue to a
   Python list for dequeue speed, exercising the circular queue’s overflow
   behaviour and testing the hash map under heavy collision load and
   validates data integrity for values exceeding 64-bit architectural limits.
   It does not alter the main simulation state.

5. **View & Clear Admin Action Log (Stack Unwind)** – Walks through the
   administrator audit log stack, popping each entry to display the most
   recent actions first.  At the end you can choose to permanently clear
   the log or restore it.  Restoring pushes the actions back onto the stack
   in reverse order so the original sequence is preserved.

6. **Discharge and Refill (Macro)** – Performs a macro cycle: it discharges
   up to three patients from the pharmacy queue (updating their status to
   “Discharged Home” and removing them from the master list), processes all
   samples in the lab buffer (marking them as analysed), then admits five
   new patients via the patient factory. New patients are added to the
   hash map and master list and the list is re‑sorted with merge sort.

7. **Logout** – Ends the session and exits the program.

------------------------------------------------------------

## Testing

A diagnostic harness is included to provide reassurance that the custom data
structures behave as expected:

* **Stability test** – Checks that the merge sort keeps patients with equal
  priority in their original arrival order.

* **Latency test** – Measures how long it takes to dequeue 10,000 patients from
  the linked queue compared with removing the first element from a Python list;
  the latter grows linearly with N whereas the linked queue stays fast.

* **Collision test** – Fills the hash map beyond its initial capacity and
  verifies that all items can still be retrieved, demonstrating effective
  collision handling and resizing.

* **Integer test** - Verifies that the system can store very large numbers
* without corruption. This test creates a node containing a value much larger
* than a 64-bit integer (using 1**100), and ensures the value is retrived intact.

These tests can be run from within the program via the diagnostics menu (option 4).
