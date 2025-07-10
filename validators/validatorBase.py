from abc import ABC, abstractmethod

class ValidatorBase(ABC):
 
    def setValidatorValues(self, testingAgent, SUT_Output, data):
        self.testingAgent = testingAgent
        self.SUT_Output = SUT_Output
        self.data = data
    
    @abstractmethod
    def validate(self):
        pass
    
