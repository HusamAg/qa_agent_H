from agents.testing_agent import TestingAgent

class WhitelistValidator:
    def __init__(self):
        pass

    def setValidatorValues(self, testingAgent, SUT_Output, data):
        self.testingAgent = testingAgent
        self.SUT_Output = SUT_Output
        self.data = data

    def validate(self):
        print(f"Running WhitelistValidator with SUT Output: {self.SUT_Output}\n\ndata: {self.data}")
        for testCaseQuestion in self.data:
            wlPrompt = "providing the following answer from an AI model \"" + self.SUT_Output + "\". Answer This question: " + testCaseQuestion
            testingAgentResponse = self.testingAgent.run_sync(wlPrompt)
            if "No" in testingAgentResponse.output:
                return False
        return True