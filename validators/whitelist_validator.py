from validators.validatorBase import ValidatorBase


class WhitelistValidator (ValidatorBase):
    
    def validate(self):
        print(f"Running WhitelistValidator with AUT Output: {self.AUTOutput}\n\ndata: {self.data}")
        # update with pydantic
        wlPrompt = "providing the following answer from an AI model \'" + self.AUTOutput + "\'. Answer these question in separated lines: " + " ".join(self.data)
        testingAgentResponse = self.testingAgent.run_sync(wlPrompt)
        return "No" not in testingAgentResponse.output.split("\n")