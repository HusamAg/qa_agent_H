import ollama
import json


DEFAULT_Q = 5 # total number of trials per prompt (if not defined in json)
DEFAILT_A = 1 # Accuracy of answer (average yes over all prompts sent) (if not defined in json)
Q = DEFAULT_Q
A = DEFAILT_A
TESTING_AGENT = "qa_tester_v0"
test_cases_file = 'Test_cases/Test_cases_chunk_2.json'

def logging(msgs):
    print("-"*20)
    for msg in msgs:
        print(msg)
    print("-"*20)


def runTestCase(SUT, testCase):
    Q = DEFAULT_Q
    A = DEFAILT_A
    total_passed_cases = 0
    if "Q" in testCase:
        Q = testCase["Q"]
    if "A" in testCase:
        A = testCase["A"]
    for i in range(Q):
        # Call SUT and pass prompt to it
        messages = [{
            'role': 'user', 
            'content': testCase["prompt"]
        }]
        response = ollama.chat(model=SUT, messages=messages)
        logging(["--SUT RESPONSE--", response['message']['content']])
        # Validate the output vs all whitelist and blacklist questions using TESTING_AGENT
        # Checking whitelist
        whitelist_pass = 1
        for item in testCase["whitelist"]:
            WL_messages = [{
                'role': 'user', 
                'content': "providing the following answer from an AI model\""+ response['message']['content'] +"\". Answer This question: " + item
            }]
            res = ollama.chat(model=TESTING_AGENT, messages=WL_messages)
            logging(["--TESTING AGENT WHITELIST--", "Prompt: providing the following answer from an AI model \""+ response['message']['content'] +"\". Answer This question: " + item, TESTING_AGENT + ": " + res['message']['content']])
            # fail on whitelist means test case failure
            if "No" in res['message']['content']: 
                whitelist_pass = 0
                break
        blacklist_pass = 1
        for item in testCase["blacklist"]:
            BL_messages = [{
                'role': 'user', 
                'content': "providing the following answer from an AI model \""+ response['message']['content'] +"\". Answer This question: " + item
            }]
            res = ollama.chat(model=TESTING_AGENT, messages=BL_messages)
            logging(["--TESTING AGENT BLACKLIST--", "Prompt: providing the following answer from an AI model \""+ response['message']['content'] +"\". Answer This question: " + item, TESTING_AGENT + ": " + res['message']['content']])

            # if only single blacklist item returns Yes, we wil mark the whole trial as blacklist and fail it
            if "Yes" in res['message']['content']: 
                blacklist_pass = 0
                break
        if whitelist_pass and blacklist_pass:
            total_passed_cases += 1
    # test case summary
    logging(["--TEST CASE SUMMARY--", "Test case id: " + str(testCase["id"]), "Total passed cases: " + str(total_passed_cases), "Q: " + str(Q), "A: " + str(A), "Actual accuracy: " + str(total_passed_cases / Q)])
        
    if total_passed_cases / Q < A:
        return False
    return True

# Open the JSON file in read mode ('r')
with open(test_cases_file, 'r') as file:
    # Load the JSON data from the file
    test_cases_data = json.load(file)

if not test_cases_data:
    print("No test cases provided!")
    exit

for value in test_cases_data["TestCases"]:
    tc_result = runTestCase(test_cases_data["SUT"], value)
    print("Test case id " + str(value["id"]) + ": " + str(tc_result))