import os
import importlib.util
import json

from agents.sut_agent import SUTAgent
from agents.testing_agent import TestingAgent

class TC_Runner:
    def __init__(self, testCases, SUT, testingAgent, Q=5, A=1):
        self.Q = Q
        self.A = A
        self.testCases = testCases
        self.SUT = SUTAgent(SUT["model"], SUT["provider"])
        self.testingAgent = TestingAgent(testingAgent["model"], testingAgent["provider"])
        self.testCasesOutput = {}
        self.validators = self.initValidators()
    
    def initValidators(self):
        validators = {}
        directory_path = "./validators/"
        for filename in os.listdir(directory_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]  # Remove .py extension
                try:
                    # Use importlib.util for more controlled importing
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory_path, filename))
                    if spec:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        validators[module_name] = module
                        print(f"Successfully imported module: {module_name}")
                except Exception as e:
                    print(f"Error importing {filename}: {e}")
        return validators
    
    def runTestCase(self, test_case):
        if "Q" in test_case:
            Q = test_case["Q"]
        else:
            Q = self.Q
        if "A" in test_case:
            A = test_case["A"]
        else:
            A = self.A
        totalPassedAttempts = 0
        # run all validators in test case.
        for i in range(Q):
            attemptStatus = True
            sut_response = self.SUT.run_sync(test_case["prompt"])
            for validatorToRun in test_case["validators"]:
                validatorFile, validatorClassName = validatorToRun["name"].split('.')
                if validatorFile not in self.validators:
                    print(f"Validator {validatorToRun} not found!")
                    continue
                validatorObj = getattr(self.validators[validatorFile], validatorClassName)()
                validatorObj.setValidatorValues(self.testingAgent, sut_response.output, validatorToRun["data"])
                validatorStatus = validatorObj.validate()
                if not validatorStatus:
                    attemptStatus = False
                    print(f"Validator {validatorToRun['name']} failed for test case {test_case['name']}")
                    break
            if attemptStatus:
                totalPassedAttempts += 1
        if totalPassedAttempts / Q < A:
            print(f"Test case {test_case['name']} failed with accuracy {totalPassedAttempts / Q}")
            return False
        return True

    def run(self):
        for testCase in self.testCases:
            print(f"Running test case: {testCase['name']} | id: {testCase['id']}")
            self.testCasesOutput[testCase["id"]] = {}
            self.testCasesOutput[testCase["id"]]["name"] = testCase["name"]
            self.testCasesOutput[testCase["id"]]["result"] = self.runTestCase(testCase)
    
    def printTestCasesOutput(self):
        print("Test Cases Output:")
        print(json.dumps(self.testCasesOutput, indent=4))