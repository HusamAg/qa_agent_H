import sys
import json

from tc_runner import TC_Runner
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <test_cases_file>")
        sys.exit(1)

    test_cases_data = {}
    with open(sys.argv[1], 'r') as file:
        test_cases_data = json.load(file)

    if not test_cases_data:
        print("No test cases provided!")
        sys.exit(1)
    # preparing tc_runner 
    tc_runner = TC_Runner(test_cases_data["TestCases"], test_cases_data["SUT"], test_cases_data["TestingModel"])
    tc_runner.run()
    tc_runner.printTestCasesOutput()

    
    