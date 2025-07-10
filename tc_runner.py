import os
import importlib.util
import json

from agents.aut_agent import AUTAgent
from agents.testing_agent import TestingAgent

class TC_Runner:
    def __init__(self, testCases, AUT, testingAgent, timesToRepeat=5, acceptedAccuracy=1):
        self.timesToRepeat = timesToRepeat
        self.acceptedAccuracy = acceptedAccuracy
        self.testCases = testCases
        self.AUT = AUTAgent(AUT["model"], AUT["provider"])
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
        if "timesToRepeat" in test_case:
            timesToRepeat = test_case["timesToRepeat"]
        else:
            timesToRepeat = self.timesToRepeat
        if "acceptedAccuracy" in test_case:
            acceptedAccuracy = test_case["acceptedAccuracy"]
        else:
            acceptedAccuracy = self.acceptedAccuracy
        totalPassedAttempts = 0
        # run all validators in test case.
        for i in range(timesToRepeat):
            attemptStatus = True
            aut = self.AUT.run_sync(test_case["prompt"])
            for validatorToRun in test_case["validators"]:
                validatorFile, validatorClassName = validatorToRun["name"].split('.')
                if validatorFile not in self.validators:
                    print(f"Validator {validatorToRun} not found!")
                    continue
                validatorObj = getattr(self.validators[validatorFile], validatorClassName)()
                validatorObj.setValidatorValues(self.testingAgent, aut.output, validatorToRun["data"])
                validatorStatus = validatorObj.validate()
                if not validatorStatus:
                    attemptStatus = False
                    print(f"Validator {validatorToRun['name']} failed for test case {test_case['name']}")
                    # add option to allow proceeding with next validator
                    break
            if attemptStatus:
                totalPassedAttempts += 1
        if totalPassedAttempts / timesToRepeat < acceptedAccuracy:
            print(f"Test case {test_case['name']} failed with accuracy {totalPassedAttempts / timesToRepeat}")
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