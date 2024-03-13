Database
========

ClassDatabase
-------------

Classes and their Methods
~~~~~~~~~~~~~~~~~~~~~~~~~

Parameters
++++++++++

    +------------+----------+-------------------------------------------------------------------------------------------------------------------------+
    |Name        |Type      |Description                                                                                                              |
    +============+==========+=========================================================================================================================+
    |class_name  | String   | This variable is the directory for the student data sets. Its the name of the table that all the students' data is kept.|
    +------------+----------+-------------------------------------------------------------------------------------------------------------------------+
    |student_id  | Integer  | Gives the database the students last name, applying it to the student ID number.                                        |
    +------------+----------+-------------------------------------------------------------------------------------------------------------------------+
    |first_name  | String   | Gives the data base the students first name, applying/overriding the students data set.                                 |
    |            |          |                                                                                                                         |
    |            |          | it can be called anytime to bring up the students data set.                                                             |
    +------------+----------+-------------------------------------------------------------------------------------------------------------------------+
    |last_name   | String   | This parameter controls the student data sets, creating/overriding the students data set.                               |
    |            |          |                                                                                                                         |
    |            |          | it can be called anytime to bring up the students data set.                                                             |
    +------------+----------+-------------------------------------------------------------------------------------------------------------------------+
    |photo_path  | String   | This controls the path directory for the students photo.|
Functions
+++++++++


create_students 
^^^^^^^^^^^^^^^
    The create_student method creates a new student record in the database by inserting the provided first name and last name into the "students" table. It then commits the changes to the database and returns the ID of the newly created student record, or None if an error occurs. If an exception is caught during the execution, it logs the error and returns None.
    
    
    Using the parameters below you can form the students information.
        create_student(first_name: str, last_name: str)
        +------------+----------+-----------------------------------------------------------------------------------------------------------------+
        |Name        |Type      |Description                                                                                                      |
        +============+==========+=================================================================================================================+
        |class_name  |String    | This variable is the directory for the data. Its the name of the table that all the students' data is formatted.|
        +------------+----------+---------------------------+
        |first_name  |String    | 
        +    first_name - string, adds a first name to the students data.
        |Last Name   | String   | Gives the database the students last name, applying it to the student ID number.|
        +    last_name - string, adds a last name to the students data.


update_students
^^^^^^^^^^^^^^^

User
~~~~

.. autoclass:: ClassDatabase
    :members: