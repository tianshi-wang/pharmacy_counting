# Table of Contents
1. [Description](README.md#description)
2. [Highlights](README.md#highlights)
3. [Run the code](README.md#Run-the-code)
4. [Test](README.md#test)
5. [Code Structure](README.md#code-structure)
6. [Contacts](README.md#contacts)

# Problem

This Python3 code is written for the coding chanllenge of Insight. As required, the code generates a list of all drugs, the total number of UNIQUE individuals who prescribed the medication, and the total drug cost. The list is in descending order based on the total drug cost and if there is a tie, drug name. 


# Highlights

1. Good scalability. The code process the 1.1 GB sample file in ~65 seconds without showing significantly slow-down as a function of the number of records 
2. The maximum memory usage is lowered by storing self-defined prescriber_ID instead of prescriber_name. For the sample file with size of 1.1 GB, the maximum memory usage is reduced to ~1 GB from ~2.2 GB.
3. Defensively coded: ability to handle corrupt records such as missing or invalid data and to output useful information 
4. Tested for different situations  

# Run the code

To run the code, go to the pharmacy_counting folder and run the ./run.sh:
    pharmacy_counting~$ ./run.sh 

The output can be found at pharmacy_counting/output/top_cost_drug.txt
The output file contains comma (`,`) separated fields of drug_name, num_prescriber, and total_cost

# Test

Five tests are included:

**Test_1**: test file provided by Insight;

**Test_2**: test whether the code can handle records with "*,*" such as '1000000004,"Rodriguez, MD",Maria,"CHLORPROMAZINE 5,000",2000';

**Test_3**: test whether the code can pass missing data, such as '1000000004,Maria,CHLORPROMAZINE,2000'

**Test_4**: test if the code passes invalid data: '1000000004,Rodriguez,Maria,CHLORPROMAZINE,2000$'

**Test_5**: test sorting by cost and drug_name in descending

To run the test, bash the run_tests.sh file in insight_testsuite
    pharmacy_counting/insight_testsuite~$ ./run_tests.sh 

# Code Structure


    ├── README.md 
    ├── run.sh
    ├── src
    │   └── pharmacy-counting.py
    ├── input
    │   └── itcont.txt
    ├── output
    |   └── top_cost_drug.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── itcont.txt
            |   |__ output
            |   │   └── top_cost_drug.txt
            . . .
            . . .
            . . .
            . . . 
            . . .
            ├── test_5
                ├── input
                │   └── itcont.txt
                |── output
                    └── top_cost_drug.txt


# Contacts

Please feel free to reach out over email (tswang@udel.edu).

Hope to hear from you soon,


Tianshi Wang

https://tswang.wixsite.com/home

https://github.com/tianshi-wang/
