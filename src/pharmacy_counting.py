"""
This module processes an input file and generates a list of all drugs, the total number of UNIQUE individuals
who prescribed the medication, and the total drug cost. 

Input file:
    The input file is in the following format:
    id,prescriber_last_name,prescriber_first_name,drug_name,drug_cost
    1000000001,Smith,James,AMBIEN,100
    1000000002,Garcia,Maria,AMBIEN,200

Output file:
    The output file, 'top_cost_drug.txt', is located in 'output' folder containing the following fields in each line. 
    drug_name(str): the exact drug name as shown in the input dataset
    num_prescriber (int): the number of unique prescribers who prescribed the drug. 
    total_cost(int): total cost of the drug across all prescribers 
"""

import sys
import time
import re

def parse_line(line):
    """
    Parse a single record. Called by process_input_file()
    Args:
        line(str): a line in input_file with '\n' striped.
    Return:
        drug_name(str), drug_cost(float), prescriber_name(firstName_lastName)
    """
    line = line.rstrip('\n')
    record =  line.rsplit(',') if '"' not in line else parse_line_with_quotation(line)
    if len(record)!=5:  #Defensive coding: Check if the record misses value.
        print("Error reading a record. Please check this line: "+line)
        return None
    try:
        drug_cost = float(record[-1])  #
    except:
        print("Error when converting drugName_to_cost to float. Check record: "+line)
        return None
    last_name, first_name, drug_name = record[1:-1]
    prescriber_name = first_name+'_'+last_name
    return drug_name, drug_cost, prescriber_name

def parse_line_with_quotation(line):
    """
    Parse a line if it has quotations e.g. '1000000003,Johnson,James,"CHLORPROMAZINE 5,000",1000'.
    Args:
        line: a line in input_file with '\n' striped.
    Return:
        record: a list contains [0]:prescriber_id, [1]: last_name, [2]: first_name, [3]: cost and [4] drug_name
    """
    def commarepl(matchobj):    # Substitute matched objects which has '" , "' patterns with '#*#'
        tmp = matchobj.group(0)
        tmp = tmp.replace("\"", '')
        tmp = tmp.replace(",", "#*#")
        return tmp
    line = re.sub('\".*?,.*?\"', commarepl, line) # Substitute matched objects which has '" , "' patterns with '#*#'
    record = line.split(',')    # Split the line by ','. The comma inside quotations have been substituted by #*#.
    record = [seg.replace("#*#", ",") for seg in record]   # Change #*# back to ,
    return record

def process_input_file(input_file):
    """
    Process input file line by line. Each line is parsed by calling parse_line function.
    The parsed results are then processed by internal functions 'reducer' and 'encode_prescriberName'.
    Args:
        input_file: the route of input file assigned by argv[1]
    Return:
         drugName_to_prescriberID: A dictionary like {'drug_name':['unique_prescriber1_id','prescriber2_id','etc']}
         drugName_to_cost: A dictionary like {'drgu_name':total_drugName_to_cost}
    Internal functions:
        reducer: Update drug_to_cost and drugName_to_prescriberID dictionaries after parsing a line.
        encode_prescriberName: Convert a prescriber_name to a unique prescriberID to save memory.
    """
    try:
        file = open(input_file, 'r')
    except:
        print ('Failed to open the dataset. Please check your input.')
        return 0
    drugName_to_cost = {}  #To store the total_cost for each drug.
    drugName_to_prescriberID = {}  #To store the unique prescriber set for each drug
    prescriberName_to_ID = {}  #To store the self-defined ID for each prescriber.
    num_correct_line = 0   #The number of corrupt records which is defined as 'cost not float' and 'length not 5'.
    maxID = 0    #The number of unique prescribers. Will be updated as record reading.

    def reducer(new_record):
        """
        Updates drug_to_cost and drugName_to_prescriberID dictionaries for each record
        Args:
            record: (drug_name, cost, prescriber_name) for each parsed line.
        Return:
            Updated drug_to_cost and drugName_to_prescriberID by the new record.
        """
        drug_name, cost, prescriber_name = new_record
        try:
            drugName_to_cost[drug_name] += cost  # If pass, drug_name is also in drugName_to_prescriberID.
            drugName_to_prescriberID[drug_name].add(prescriber_name)
        except KeyError:  # Raised when drug_name is not in drugName_to_cost
            drugName_to_cost[drug_name] = cost
            drugName_to_prescriberID[drug_name] = {prescriber_name}

    def encode_prescriberName(prescriber_name, maxID):
        """
        Convert prescriberName to a self-defined ID to save memory.
        Args:
            prescriber_name: A string in the format: firstName_lastName
            maxID: int, +1 after adding a new prescriber_name to the dictionary keys.
        Return:
            The corresponding id for the given name and the updated maximum ID.
        """
        try:
            prescriberID = prescriberName_to_ID[prescriber_name]
            return prescriberID, maxID
        except KeyError:
            prescriberName_to_ID[prescriber_name] = maxID
            maxID += 1
            return maxID-1, maxID

    next(file)  #pass the first line.
    print("Start reading input file.")
    for line in file:
        try:
            drug_name, drug_cost, prescriber_name = parse_line(line)   # Process a single line.
        except TypeError: # Raise TypeError if parse_line returns None
            num_correct_line += 1
            continue     # Skip this line if parse_line returns None.
        prescriberID, maxID = encode_prescriberName(prescriber_name, maxID)  #Convert name to ID.
        reducer(new_record = (drug_name, drug_cost, prescriberID))   #Add the information to dictionaries.
    print("The number of corrupt records is "+str(num_correct_line)+".")
    drugName_to_cost = {key:round(value) for key, value in drugName_to_cost.items()} #Convert tot_cost from float to int
    drugName_to_numPrescriber = {key:len(value) for key, value in drugName_to_prescriberID.items()} #List to its length.
    file.close()
    return drugName_to_numPrescriber, drugName_to_cost

def sort_by_cost(drugName_to_prescriberID, drugName_to_cost):
    """
    Sort the dictionaries (drugName_to_cost and drugName_to_prescriberID by cost(1st, desc) and by drug_name(2nd).
    Args:
        drugName_to_prescriberID: prescriberID is a list which already contains records from all lines.
        drugName_to_cost: cost is an integer which sums up the cost by all prescribers.
    Return:
        output_str: sorted output_string which in the same format as output file.
    """
    output_str = 'drug_name,num_prescriber,total_cost\n'
    for drug_name in sorted(drugName_to_cost, key= lambda x: (drugName_to_cost[x], x), reverse=True):
        output_str += drug_name+','+str(drugName_to_prescriberID[drug_name])+\
                      ','+str(drugName_to_cost[drug_name])+'\n'
    print("Results have been sorted by cost and drug_name.")
    return output_str

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    start = time.time()
    drugName_to_numPrescriber, drugName_to_cost = process_input_file(input_file) # Process input file line by line.
    output_str = sort_by_cost(drugName_to_numPrescriber, drugName_to_cost) # Sort and combine the two dictionaries.
    with open(output_file, 'w') as output_file:
        output_file.write(output_str)
    print("Totel running time is "+ str(round(time.time()-start))+" seconds.")

if __name__=='__main__':
    sys.argv.append( '../input/itcont.txt')
    sys.argv.append( '../output/top_cost_drug.txt')
    main()



