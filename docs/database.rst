Database
========


Classes and their Methods
-------------------------

ClassDatabase
~~~~~~~~~~~~~

Parameters
++++++++++

class_name
^^^^^^^^^^
    This vairable is attached to the data set that holds the student data.
    This variable must be a string, it is the name of the table that the student data will be stored under.
student_id
^^^^^^^^^^
    holds the student identitiy numbers.
    
    this variable is linked to an integer and can be any real-whole number that has a value higher than 0.

Functions
+++++++++

.. note::        
    Self is something that all the definitions use, this can be ignored.

create_students 
^^^^^^^^^^^^^^^
    This is called to create a brand new student, this is the first step of the student data process.
    
    
    Using the parameters below you can form the students information.
        create_student(first_name: str, last_name: str)
        class_name - directs which table the data needs to be put under.
        first_name - string, adds a first name to the students data.
        last_name - string, adds a last name to the students data.

update_students
^^^^^^^^^^^^^^^

User
~~~~

.. autoclass:: ClassDatabase
    :members: