This is a python program for parsing csv files and providing details on the aggregate data.

Produced by: Ryan Tonini


Folder Structure
----------------

    .                 
    ├── rendparse			    # Python source files 
    │   ├── __init__.py         # To mark the directory
    │   ├── entry.py            # Entry point of application
    │   ├── helpers.py          # Miscellaneous functions 
    │   ├── parser.py           # Core classes and functions 
    ├── run.sh                  # Bash script to run application 
    ├── Makefile				# To build application
    └── README.md      			# Information on how to use the project


Usage
-----

Navigate to the root directory of this project.  Then run

    ./run.sh

 to execute the application.  This script may be passed any arguments that were specified in the requirements file.


 Note
-----

For simplicity in the build process, I only used standard python libraries.  Better efficiency can be achieved by employing third party libraries like Numpy and Pandas.  