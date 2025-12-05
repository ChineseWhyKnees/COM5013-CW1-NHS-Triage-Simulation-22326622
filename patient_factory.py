"""
FILE: patient_factory.py
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

DESCRIPTION:
    Implements the Factory Method design pattern for PatientRecord instantiation.
    
    ARCHITECTURAL JUSTIFICATION (LO3):
    Encapsulation:
    Abstracts the complexity of object construction from the client (Main Loop).
    The client requests a patient, and the factory handles the stochastic 
    assembly details.
    
    Decoupling:
    Separates the Data Model (PatientRecord) from the Data Source (Generator).
    This allows for consistent testing; we can swap the generator with a 
    mock object to produce deterministic patients for unit testing without 
    modifying the record class itself.
    
    State Management:
    Maintains a sequential counter for NHS Numbers to guarantee uniqueness
    during initialisation, preventing hash collisions before the LCG takes over.
"""

from patient_generator import patientdatagenerator
from patient_record import patientrecord

class patientfactory:
    """
    Factory class responsible for assembling valid PatientRecord objects.
    """
    
    def __init__(self, generator: patientdatagenerator, seed: int = 42):
        """
        Configures the factory instance.
        
        Args:
            generator (patientdatagenerator): The stochastic data provider.
            seed (int): Initial seed for the factory-specific LCG (Priority generation).
        """
        self.generator = generator
        
        # LCG State specifically for Priority generation (distinct from generator utility)
        self.factory_seed = seed
        
        # Sequential counter to guarantee Unique ID (Hash Key) uniqueness
        self.nhs_counter = 0

    def _get_next_pseudo_random(self, max_val: int) -> int:
        """
        Internal LCG for generating numeric attributes (Priority).
        """
        self.factory_seed = (self.factory_seed * 1103515245 + 12345) % (2**31)
        return self.factory_seed % max_val
    
    def _create_unique_nhs_number(self) -> str:
        """
        Generates a guaranteed unique NHS number via incrementation.
        Essential for avoiding collisions during initial HashMap population tests.
        """
        self.nhs_counter += 1
        return str(self.nhs_counter)

    def create_patient(self) -> patientrecord:
        """
        Constructs and populates a single PatientRecord instance.
        
        Integrates the unique identifier (Factory responsibility) with 
        stochastic demographic data (Generator responsibility).
        
        Returns:
            patientrecord: A fully initialized object with populated history log.
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
    print("--- Initializing Factory Architecture ---")
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