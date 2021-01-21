# Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Command Line](#command-line)
- [Algorithms](#algorithms)

# Introduction

CPrefSQL is a prototype extension for the PostgreSQL database management system (DBMS)  with support to conditional preferences queries [CPrefSQL Project](http://cprefsql.github.io).

A normal SQL query is executed, returning the tuples, which are then processed by the CPrefSQL operators following the preferences defined in an input file.
The file content must follow the CPrefSQL grammar (see file __grammar/cprefsql.ebnf__).
Example of an query file with conditional preferences:

```
(brand = 'Apple') BETTER (brand = 'Samsung')[screen,model,ram,storage,price]
AND
(brand = 'Samsung') BETTER (brand='Motorola') [screen,model, ram, storage, price]
AND
IF (brand = 'Samsung')  THEN (ram <6) > (ram>=6) [screen,model,storage,price]
```

Please see the directory __algorithms__ for more examples.

# Command Line
In their current form, using SQLite as the DBMS, the algorithms can be tested by running the test run files in the directory __algorithms__, they follow the naming convention of "test_"+(algorithm name)+".py".  They all have the same command line interface, with three parameters: the preference file, the SQLite database and the table in the database that will be searched. One example of the command line interface used:
```
test_nested_loops.py PREFFILE DATABASE TABLE
    
    PREFFILE                                File containing the preferences defined by the user, following CPrefSQL grammar
    DATABASE                                File containing the SQLite database
    TABLE                                   Table name to be used in the query
```
The algorithms can also be used in any other application by just importing the packages. Assuming the correct directory have been added to **PYTHONPATH**.

# Installation
To install CPrefSQL, copy  the content of this repository to any directory of your choice and add the directory absolute path to the **PYTHONPATH** environment variable using the following command on the terminal:
```
export PYTHONPATH="${PYTHONPATH}:/my/cprefsql/path"
```
For a permanent change, consider editing file ~/.pythonrc on your user directory.

# Algorithms
By choosing the corresponding test file, the user can choose an algorithm to evaluate the operators. To choose the operation between the operators __BEST__ and __TOPK__, please edit the test files.  The evaluations of the operators can be performed by the following algorithms:
- *nested_loops*: Block Nested Loops (BNL);
- *partition*: Preference partition algorithm;
- *maxpref*: Partition based algorithms with new hierarchy model based on maximal level.

Please see the related publications for more information.
