from abc import ABC, abstractmethod

class ValidatorBase(ABC):
 
    def setValidatorValues(self, testingAgent, AUTOutput, data):
        self.testingAgent = testingAgent
        self.AUTOutput = AUTOutput
        self.data = data
    
    @abstractmethod
    def validate(self):
        pass
    
