from validators.validatorBase import ValidatorBase


class BlacklistValidator (ValidatorBase):
    
    def validate(self):
        print(f"Running BlacklistValidator with AUT Output: {self.AUTOutput}\n\ndata: {self.data}")
        # update with pydantic
        wlPrompt = "providing the following answer from an AI model \'" + self.AUTOutput + "\'. Answer these question in separated lines: " + " ".join(self.data)
        testingAgentResponse = self.testingAgent.run_sync(wlPrompt)
        return "Yes" not in testingAgentResponse.output.split("\n")