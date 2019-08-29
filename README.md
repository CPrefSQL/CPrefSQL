# Table of Contents

- [Introduction](#introduction)
- [Command Line](#command-line)
- [Algorithms](#algorithms)

# Introduction

CPrefSQL is a prototype extension for the PostgreSQL database management system (DBMS)  with support to conditional preferences queries [CPrefSQL Project](http://cprefsql.github.io).

A normal SQL query is executed, returning the tupples, which are then processed by the CPrefSQL operators following the preferences defined in an input file.
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
In their current form, using SQLite as the DBMS, the algorithms can be tested by running the test run files in the directory __algorithms__, they follow the naming convesion of "test_"+(algorithm name)+".py".
They all have the same command line interface, with three parameters: the preference file, the SQLite database and the table in the database that will be searched.
Example of the command line interface used:
```
test_nested_loops.py PREFFILE DATABASE TABLE
    
    PREFFILE                                File containing the preferences defined by the user, following CPrefSQL grammar 
    DATABASE                                File containing the SQLite database
    TABLE                                   Table name to be used in the query
```

# Algorithms
By choosing the corresponding test file, the user can choose an algorithm to evaluate the operators __BEST__ and __TOPK__.
The evaluations of the operators can be performed by the following algorithms:
- *nested_loops*: Block Nested Loops (BNL);
- *partition*: Preference partition algorithm;
- *formulas*: Formula comparison based algorithm.


Please see the related publications for more information.
