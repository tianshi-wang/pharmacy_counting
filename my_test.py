import sys
import unittest
import filecmp
sys.path.append('../src')
from pharmacy_counting import *

class MyTest(unittest.TestCase):
    def test_process_line(self):
        # Test four different kinds of records
        test_line0 = '1063421576,ABRAHAM,CINI,VENLAFAXINE HCL ER,389.04'    #without " ".
        corr_result0 = ('VENLAFAXINE HCL ER',389.04,'CINI_ABRAHAM')

        test_line1 = '1063421576,"ABRAHAM, M.D.",CINI,VENLAFAXINE HCL ER,389.04'    #with one " ".
        corr_result1 = ('VENLAFAXINE HCL ER',389.04,'CINI_ABRAHAM, M.D.')

        test_line2 = '1063421576,"ABRAHAM, M.D.",CINI,"VENLAFAXINE HCL ER 5,000",389.04'    #with  two " ".
        corr_result2 = ('VENLAFAXINE HCL ER 5,000',389.04,'CINI_ABRAHAM, M.D.')

        test_line3 = '1063421576,"ABRAHAM, M.D.","CINI,VENLAFAXINE HCL ER 5,000",cost_not_float'    #Corrupt records
        corr_result3 = None

        self.assertEqual(process_line(test_line0),corr_result0)
        self.assertEqual(process_line(test_line1),corr_result1)
        self.assertEqual(process_line(test_line2),corr_result2)
        self.assertEqual(process_line(test_line3),corr_result3);


    def test_read_input_file(self):
        #Check if read_input_file function can convert records to the expected dictionaries.
        input_file="./tests/my_test/input/itcont.txt"
        drugName_to_prescriberID, drugName_to_cost = read_input_file(input_file)
        corr_drugName_to_prescriberID = {'AMBIEN': {0, 1}, 'CHLORPROMAZINE': {2, 3}, 'BENZTROPINE MESYLATE': {0}}
        corr_drugName_to_cost = {'AMBIEN': 300, 'CHLORPROMAZINE': 3000, 'BENZTROPINE MESYLATE': 3000}
        self.assertEqual(drugName_to_prescriberID, corr_drugName_to_prescriberID)
        self.assertEqual(drugName_to_cost, corr_drugName_to_cost, msg="Cost is equal")

    def test_sort_by_cost(self):
        #Test if sort_by_cost can sort the two dictionaries (drugName_to_prescriberID, drugName_to_cost) correctly
        #by cost (desc) and by drug_name.
        drugName_to_prescriberID = {'AMBIEN': {0, 1}, 'CHLORPROMAZINE': {2, 3}, 'BENZTROPINE MESYLATE': {0}}
        drugName_to_cost = {'AMBIEN': 300, 'CHLORPROMAZINE': 3000, 'BENZTROPINE MESYLATE': 3000}
        output_str = sort_by_cost(drugName_to_prescriberID, drugName_to_cost)
        corr_output_str = 'drug_name,num_prescriber,total_cost\n' \
                          'CHLORPROMAZINE,2,3000\n' \
                          'BENZTROPINE MESYLATE,1,3000\n' \
                          'AMBIEN,2,300\n'
        self.assertEqual(output_str, corr_output_str)

    def test_output(self):
        output_str = 'drug_name,num_prescriber,total_cost\n' \
                          'CHLORPROMAZINE,2,3000\n' \
                          'BENZTROPINE MESYLATE,1,3000\n' \
                          'AMBIEN,2,300\n'
        output_file = './tests/my_test/output/results.txt'
        write_output(output_file, output_str)
        self.assertTrue(filecmp.cmp('./tests/my_test/output/results.txt', './tests/my_test/output/correct_results.txt'))


if __name__ == '__main__':
    unittest.main()
