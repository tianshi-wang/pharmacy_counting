test_1: test file provided by Insight.
test_2: test whether the code can handle records with "*,*" such as '1000000004,"Rodriguez, MD",Maria,"CHLORPROMAZINE 5,000",2000'.
test_3: test whether the code can pass missing data, such as '1000000004,Maria,CHLORPROMAZINE,2000'
test_4: test if the code passes invalid data: '1000000004,Rodriguez,Maria,CHLORPROMAZINE,2000$'
test_5: test sorting by cost and drug_name in descending
