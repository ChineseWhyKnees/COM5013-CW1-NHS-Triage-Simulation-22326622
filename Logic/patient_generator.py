"""
FILE: patient_generator
AUTHOR: 22326622
MODULE: COM5013 Algorithms & Data Structures

This module supplies the raw ingredients for building patient records.
It defines a simple **linear congruential generator (LCG)**, a lightweight
algorithm for producing sequences of numbers that appear random. These
numbers are used to pick items from static lists of first names, last names,
dates of birth, ailments, symptoms, medications and blood types. By
providing its own random number generator rather than using Python's
``random`` module, the codebase gains two important properties:

* **Determinism:** if the initial seed is the same, the sequence of numbers
  produced by the LCG (and therefore the sequence of selected names and
  attributes) will also be the same. This is helpful when testing the
  simulation because it makes runs repeatable.
* **Simplicity:** an LCG keeps only a single integer in memory, making it
  easy to understand and predict. The bigger Mersenne Twister engine used
  by Python's ``random`` module is more complex and has a much larger
  internal state.

The :class:`patientdatagenerator` class defined here is used by
:class:`Logic.patient_factory.patientfactory` to assemble complete patient records.
Other modules never need to interact with the LCG directly; they simply call
methods on this class to pick items from its data lists.
"""

class patientdatagenerator:
    """
    Generate pseudo-random patient attributes from fixed lists.

    An instance of this class maintains its own internal state (the LCG
    seed) and exposes helper methods to choose single items or multiple
    items from the provided datasets. The lists themselves are never
    modified; repeated calls to pick from them will simply return different
    elements. Because the same seed will always produce the same sequence
    of indices, you can get predictable results for testing by
    initialising the generator with a known seed.

    The underlying random number formula used here is

        ``X_{n+1} = (a * X_n + c) % m``

    where ``a``, ``c`` and ``m`` are fixed constants chosen to give good
    statistical properties. You do not need to understand the mathematics to
    use this class; it is sufficient to know that it produces a stream of
    seemingly random numbers.
    """

    def __init__(self, seed=12345):
        """
        Create a new generator with optional initial seed.

        Parameters:
            seed: an integer used to start the linear congruential generator.
                If you provide the same seed on different runs, the order
                of items returned by the random pick methods will also be
                identical. The default seed (12345) is arbitrary; you can
                change it to vary the pseudo-random sequence.

        During initialisation the generator also defines several lists of
        possible values for patient attributes. These datasets are stored
        directly in the object to avoid the need for external files. They
        include names, medical conditions, symptoms, medications, dates of
        birth and blood types. The lists are constant and are not altered
        when sampling from them.
        """
        self.seed = seed
        
        # --- STATIC DATASETS ---
        # Hardcoded to act as the 'DNA' for patient generation.
        # These lists eliminate the need for external file I/O dependencies.
        
        # Dataset: Pathologies and Ailments
        self.ailments = [
            "Fever", "Headache", "Cough", "Fatigue", "Nausea", "Vomiting", "Diarrhea",
            "Sore Throat", "Congestion", "Chills", "Dizziness", "Loss of Appetite",
            "Rash", "Muscle Pain", "Joint Pain", "Back Pain", "Stomach Pain"
        ]
        # Dataset: Clinical Symptoms
        self.symptoms = [
            "High Temperature", "Chronic Cough", "Persistent Nausea",
            "Persistent Vomiting", "Persistent Diarrhea", "Sputum Production",
            "Swollen Lymph Nodes", "Swollen Glands", "Swollen Skin",
            "Swollen Muscles", "Swollen Joints", "Swollen Back",
            "Swollen Stomach", "Swollen Lungs", "Swollen Kidneys"
        ]
        # Dataset: Pharmacological Treatments
        self.medications = [
            "Paracetamol", "Ibuprofen", "Acetaminophen", "Aspirin", "Antihistamines",
            "Antacids", "Antifungal Medication", "Antimalarial Medication",
            "Antiviral Medication", "Blood Pressure Medication",
            "Diabetes Medication", "High Cholesterol Medication",
            "High Blood Sugar Medication", "Lipid Lowering Medication",
            "Heart Disease Medication"
        ]
        # Dataset: Demographics (First Names)
        self.first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
            "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy",
            "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
            "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
            "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
            "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
            "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
            "Nicholas", "Angela", "Eric", "Shirley", "Jonathan", "Anna", "Stephen", "Brenda",
            "Larry", "Pamela", "Justin", "Emma", "Scott", "Nicole", "Brandon", "Helen",
            "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Frank", "Debra",
            "Alexander", "Rachel", "Raymond", "Catherine", "Patrick", "Carolyn", "Jack", "Janet",
            "Dennis", "Ruth", "Jerry", "Maria", "Tyler", "Heather"]
        
        # Dataset: Demographics (Last Names)
        self.last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
            "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
            "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
            "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
            "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
            "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
            "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
            "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
            "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
            "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
            "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
            "Long", "Ross", "Foster", "Jimenez"]
        
        # Dataset: Demographics (Dates of Birth)
        self.dobs = ["1950-01-15", "1951-03-22", "1952-07-04", "1953-11-30", "1954-05-12", "1955-09-19",
            "1956-02-28", "1957-06-14", "1958-10-05", "1959-12-25", "1960-04-01", "1961-08-18",
            "1962-01-10", "1963-03-15", "1964-07-22", "1965-11-08", "1966-05-30", "1967-09-03",
            "1968-02-14", "1969-06-29", "1970-10-11", "1971-12-01", "1972-04-17", "1973-08-25",
            "1974-01-05", "1975-05-20", "1976-09-12", "1977-11-23", "1978-03-08", "1979-07-19",
            "1980-12-05", "1981-02-22", "1982-06-10", "1983-10-31", "1984-01-15", "1985-04-01",
            "1986-08-14", "1987-11-27", "1988-03-20", "1989-07-04", "1990-09-15", "1991-12-25",
            "1992-05-08", "1993-10-12", "1994-02-28", "1995-06-18", "1996-11-03", "1997-01-22",
            "1998-04-15", "1999-08-30", "2000-12-10", "2001-03-05", "2002-07-25", "2003-09-14",
            "2004-11-01", "2005-02-19", "1952-08-12", "1955-04-23", "1958-12-09", "1961-06-15",
            "1964-10-28", "1967-03-02", "1970-09-21", "1973-01-30", "1976-05-14", "1979-11-05",
            "1982-02-11", "1985-07-29", "1988-12-18", "1991-04-05", "1994-08-22", "1997-01-09",
            "1999-06-25", "2002-10-15", "2005-03-30", "1953-09-07", "1956-01-19", "1959-05-26",
            "1962-11-14", "1965-02-04", "1968-07-12", "1971-12-28", "1974-04-10", "1977-09-01",
            "1980-01-25", "1983-06-07", "1986-10-20", "1989-03-14", "1992-08-05", "1995-11-29",
            "1998-02-16", "2001-07-08", "2004-12-02", "1951-05-31", "1954-10-17", "1957-03-09",
            "1960-08-26", "1963-01-04", "1966-06-22", "1969-04-20", "1972-09-16", "1975-02-02"]
        
        self.blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

    def _generate_random_index(self, list_length: int) -> int:
        """
        Compute a new pseudo-random index for selecting from a list.

        The generator updates its internal ``seed`` using the LCG formula and
        then maps that state to a value between 0 and ``list_length - 1`` by
        taking the remainder after division. This ensures the index is
        always valid for the target list. The constants ``a``, ``c`` and
        ``m`` used in the formula are chosen for compatibility with the
        historical ANSI C standard LCG.

        Parameters:
            list_length: the length of the list you intend to sample from.

        Returns:
            An integer index suitable for use with Python list indexing.
        """
        # Update internal state
        self.seed = (self.seed * 1103515245 + 12345) % (2**31)
        
        # Map state to list bounds using modulo arithmetic
        return self.seed % list_length 

    def get_random_item(self, source_list: list):
        """
        Choose a single element from a list using the internal LCG.

        Parameters:
            source_list: a Python list of any type. If the list is empty,
                ``None`` will be returned.

        Returns:
            The element at a pseudo-random position within ``source_list``, or
            ``None`` if the list has no elements.
        """
        if not source_list:
            return None
        
        index = self._generate_random_index(len(source_list))
        return source_list[index]

    def get_random_items(self, source_list: list, count: int) -> list:
        """
        Choose multiple elements from a list using repeated LCG sampling.

        This method calls the LCG as many times as specified by ``count`` and
        collects the elements at those pseudo-random positions. The same
        element from ``source_list`` may appear more than once in the returned
        list because the generator does not track previous selections.

        Parameters:
            source_list: a Python list of any type from which items will be
                selected. If the list is empty or ``count`` exceeds the list
                length, an empty list is returned.
            count: the number of items you wish to pick.

        Returns:
            A list containing ``count`` items selected from ``source_list``.
        """
        random_items = []
        list_length = len(source_list)

        # Input validation: Ensure population exists and sample size is valid
        if list_length == 0 or count > list_length:
            return []

        for _ in range(count):
            # Deterministic selection for each item in the subset
            index = self._generate_random_index(list_length)
            selected_item = source_list[index]
            random_items.append(selected_item)

        return random_items