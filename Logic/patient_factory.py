"""
FILE: patient_factory.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

This module acts as a "factory" for creating new patient records used
throughout the NHS triage simulation. Rather than instantiating patients
directly in many places, a single "patientfactory" object centralises the
creation process. When the main program or other parts of the system need a
new patient, they ask the factory for one. The factory then:

* Pulls pseudorandom demographic information from a "patientdatagenerator" object,
  (see :mod:`Logic.patient_generator`).
* Generates a unique identifier and initial medical priority for the patient.
* Builds a new :class:`Logic.patient_record.patientrecord` instance and populates
  its history log with some initial observations.

Centralising these steps, the rest of the codebase can depend on a simple,
consistent interface (:meth:`create_patient`) and does not need to know how
names, dates of birth or other attributes are chosen. The factory also
ensures that each patient has a unique NHS number and reproducible priority
values when tested with a fixed seed. This file provides the glue
between the random data generator and the patient record class so that
new patient objects are created in a controlled and repeatable manner.
"""

from Logic.patient_generator import patientdatagenerator
from Logic.patient_record import patientrecord

class patientfactory:
    """
    Factory class responsible for assembling complete patient records.

    The factory hides the complexity of constructing an object from its users.
    In this case it wraps together the steps of generating random names and
    dates of birth, allocating a unique NHS number and priority, and then
    building a :class:`Logic.patient_record.patientrecord` object. Other parts of
    the program simply call :meth:`create_patient` to obtain a pre-made
    record without needing to understand how the details are chosen.
    """
    
    def __init__(self, generator: patientdatagenerator, seed: int = 42):
        """
        Create a new factory.

        Parameters:
            generator: a :class:`Logic.patient_generator.patientdatagenerator` instance that
                supplies random names, ailments and other demographic data. The
                factory will call methods on this generator whenever it needs a
                new piece of information.
            seed: an integer used to initialise the factory's internal linear
                congruential generator. Changing this seed will change the
                sequence of priorities assigned to patients. Keeping it
                constant across runs makes patient creation reproducible.

        The factory stores a separate seed from the generator so that the
        randomness used for priorities does not interfere with the randomness
        used for other attributes.
        """
        self.generator = generator
        
        # LCG State specifically for Priority generation (distinct from generator utility)
        self.factory_seed = seed
        
        # Sequential counter to guarantee Unique ID (Hash Key) uniqueness
        self.nhs_counter = 0

    def _get_next_pseudo_random(self, max_val: int) -> int:
        """
        Produce the next pseudo-random integer in a fixed range.

        This private method implements a simple *linear congruential generator*,
        a mathematical formula for producing a sequence of numbers that appear
        random. The result is taken modulo ``max_val`` so it always falls
        between ``0`` and ``max_val - 1``. It is used internally to pick a
        priority value for a new patient.
        """
        self.factory_seed = (self.factory_seed * 1103515245 + 12345) % (2**31)
        return self.factory_seed % max_val
    
    def _create_unique_nhs_number(self) -> str:
        """
        Allocate a brand new NHS number.

        For simplicity the factory maintains a counter that starts at zero and
        increases by one each time this method is called. Converting the
        counter to a string gives us a unique identifier for each patient. In
        the context of the simulation there is no external registry, so this
        simple approach is sufficient to ensure uniqueness.
        """
        self.nhs_counter += 1
        return str(self.nhs_counter)

    def create_patient(self) -> patientrecord:
        """
        Build a complete :class:`Logic.patient_record.patientrecord` for a new patient.

        This method performs several coordinated steps:

        1. It calls :meth:`_create_unique_nhs_number` to obtain a unique
           identifier and :meth:`_get_next_pseudo_random` to assign a priority
           level between 1 and 5 (1 being highest urgency).
        2. It asks the :class:`Logic.patient_generator.patientdatagenerator` for a random first
           name, last name, date of birth and blood type.
        3. It combines these pieces into a new
           :class:`Logic.patient_record.patientrecord` instance. The record starts
           with an entry in its history log describing its initial priority.
        4. It populates the patient's history with randomly chosen ailments
           and symptoms to simulate an initial clinical assessment.

        Returns:
            A fully initialised patient record ready to be stored in the
            database or queued for triage.
        """
        # 1. Generate Unique Identifiers and Metrics
        new_nhs_number = self._create_unique_nhs_number()
        new_priority = self._get_next_pseudo_random(5) + 1  # 1-based index
        
        # 2. Retrieve Stochastic Attributes
        first_name = self.generator.get_random_item(self.generator.first_names)
        last_name = self.generator.get_random_item(self.generator.last_names)
        dob = self.generator.get_random_item(self.generator.dobs)
        
        # 3. Instantiate Data Model
        new_patient = patientrecord(
            nhs_number=new_nhs_number,
            dob=dob,
            first_name=first_name,
            last_name=last_name,
            priority=new_priority,
            blood_type=self.generator.get_random_item(self.generator.blood_types)
        )
        
        # 4. Populate Audit Log (History)
        # Simulate initial diagnosis and symptom presentation
        ailment_list = self.generator.get_random_items(self.generator.ailments, 2)
        symptom_list = self.generator.get_random_items(self.generator.symptoms, 1)
        
        for ailment in ailment_list:
            new_patient.update_status(f"Diagnosed with: {ailment}")
            
        for symptom in symptom_list:
            new_patient.update_status(f"Showing symptom: {symptom}")

        return new_patient

if __name__ == "__main__":
    # Integration Test
    print("--- Initialising Factory Architecture ---")
    data_gen_tool = patientdatagenerator()
    patient_factory = patientfactory(generator=data_gen_tool)

    print("\n--- Executing Generation Cycle (n=100) ---")
    patient_list = []
    for _ in range(100):
        patient = patient_factory.create_patient()
        patient_list.append(patient)
        
    for patient in patient_list[:5]: # Show first 5
        print(f"CREATED: {patient}")
        print(f"STATUS: {patient.get_current_status()}")