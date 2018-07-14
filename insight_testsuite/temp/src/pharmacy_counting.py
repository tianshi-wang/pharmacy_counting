import sys
import time

# Read a single record and return the drug_name, drugName_to_cost, prescriber_name.
# Called by read_input_file()
def process_line(line):
    splitted_record=[]
    element = ''
    within_quote = False    #Will use "within_quote" to check if the char is inside quotes.
    if '"' not in line:
        splitted_record=line.rsplit(',')
    else:
        for cha in line:   #line format: "1962514471,ABAD,JORGE,"PANCRELIPASE 5,000",669.89"
            # Start to split the record by ','. Meanwhile, avoid separating drug_name like "PANCRELIPASE 5,000"
            if cha != ',' or within_quote:
                if cha !='"':
                    element += cha
                else:
                    within_quote = not within_quote
            elif not within_quote:    #If cha==',' and not within_quote, add the value before comma to the list.
                splitted_record.append(element)
                element=''   #Clear 'element'. The 'for' loop will refill it with the next value in the line.
        splitted_record.append(element)   # Add the value after the last comma to the list.
    if len(splitted_record)!=5:  #Defensive coding: Check if the record misses value.
        print("Error reading a record. Please check this line: "+line)
        return None
    else:
        try:
            drug_cost = float(splitted_record[-1])  #
        except:
            print("Error when converting drugName_to_cost to float. Check record: "+line)
            return None
    last_name, first_name, drug_name = splitted_record[1:-1]
    prescriber_name = first_name+'_'+last_name
    return drug_name, drug_cost, prescriber_name

#Read the input_file, call process_line(line), and return two dictionaries:
#1. drugName to self-defined prescriberID {'drug_name':['unique_prescriber1_id','prescriber2_id','etc']}
#2. drugName_to_cost {'drgu_name':total_drugName_to_cost}
def read_input_file(input_file):
    drugName_to_cost = {}  #To store the total_cost for each drug.
    drugName_to_prescriberID = {}  #To store the unique prescriber set for each drug
    prescriberName_to_ID = {}  #To store the self-defined ID for each prescriber.
    num_correct_line = 0   #The number of corrupt records which is defined as 'cost not float' and 'length not 5'.
    maxID = 0    #The number of unique prescribers. Will be updated as record reading.

    def reducer(record):
        (drug_name, cost, prescriber_name) = record
        # Updates drug_to_cost and drugName_to_prescriberID dictionaries for each record
        try:
            drugName_to_cost[drug_name] += cost  # If pass, drug_name is also in drugName_to_prescriberID.
            drugName_to_prescriberID[drug_name].add(prescriber_name)
        except KeyError:  # Raised when drug_name is not in drugName_to_cost
            drugName_to_cost[drug_name] = cost
            drugName_to_prescriberID[drug_name] = {prescriber_name}
        if (index+1)%1000000 ==0 :
            print("Reading line " + format(index+1, ',d') + " .")

    def encode_prescriberName(prescriber_name, maxID):
        #Convert prescriberName to a self-defined ID.
        try:
            prescriberID = prescriberName_to_ID[prescriber_name]
            return prescriberID, maxID
        except KeyError:
            prescriberName_to_ID[prescriber_name] = maxID
            maxID += 1
            return maxID-1, maxID

    with open(input_file, 'r') as input_file:
        next(input_file)
        index = 0
        print("Start reading input file.")
        for index, line in enumerate(input_file):
            try:
                drug_name, drug_cost, prescriber_name = process_line(line.rstrip('\n'))
            except TypeError: # Raise TypeError if process_line returns None
                num_correct_line += 1
                continue     # Skip this line if process_line returns None.
            prescriberID, maxID = encode_prescriberName(prescriber_name, maxID)  #Convert name to ID to reduce memory consumption.
            reducer((drug_name, drug_cost, prescriberID))   #Add the information to dictionaries.
        print("Completed input file reading. Number of records is "+format(index+1, ',d') +".")
        print("The number of corrupt records is "+str(num_correct_line)+".")
        drugName_to_cost = {key:int(value) for key, value in drugName_to_cost.items()}  #Convert tot_cost from float to integer
    return drugName_to_prescriberID, drugName_to_cost

#Sort the dictionaries (drugName_to_cost and drugName_to_prescriberID by cost(desc) and if there is a tie by drug_name(a-z).
#Called by main() and return sorted output_string.
def sort_by_cost(drugName_to_prescriberID, drugName_to_cost):
    output_str = 'drug_name,num_prescriber,total_cost\n'
    for drug_name in sorted(drugName_to_cost, key= lambda x: (drugName_to_cost[x], x), reverse=True):
        output_str += drug_name+','+str(len(drugName_to_prescriberID[drug_name]))+','+str(drugName_to_cost[drug_name])+'\n'
    print("Results have been sorted by cost and drug_name.")
    return output_str

#Write the output_string to output_file.
def write_output(output_file, output):
    with open(output_file, 'w') as output_file:
        output_file.write(output)

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    drugName_to_prescriberID, drugName_to_cost = read_input_file(input_file)
    output_str = sort_by_cost(drugName_to_prescriberID, drugName_to_cost)
    write_output(output_file, output_str)

if __name__=='__main__':
    # sys.argv.append( '../input/itcont.txt')
    # sys.argv.append( '../output/top_cost_drug.txt')
    start = time.time()
    main()
    print("Totel running time is "+ str(round(time.time()-start))+" seconds.")


