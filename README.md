<b>Welcome to qa_agent_h</b>

qa_agent_h is an AI model based on llama3.2 with a specific role of testing output from other AI models based on test cases provided.

<b>How it works?</b>

AI models are indecisive sometimes, that means if you ask the same prompt multiple times, you can't guarantee having same exact answer everytime. This means you can't simply put a test case that provides a prompt and expects a specific answer from the AI model.
The idea is to create an LLM as a judge that can decide if this prompt passes test or not.

Test_cases/Test_cases_example.json file describes the test cases for specific model
```
  {
    "SUT": "llama3.2:latest",
    "TestCases":[
        {
            "id": 1,
            "Q": 2,
            "A": 0.5,
            "prompt":"Who are you?",
            "whitelist":[
                "Does the output mention it is an AI or related to it?",
                "Does the output mention it is a language model?"
            ],
            "blacklist":[
                "Does the output contain 'Husam'?"
            ]
        }
    ]
    
}
```
"SUT"        : The Subject Under Test, which is the model we are currently testing.<br>
"id"         : Test case id<br>
"Q"          : How many times should the same test case repeat<br>
"A"          : Acceptable accuracy of testing (total_pass_attempts / Q must be >= A)<br>
"prompt"     : The prompt to be tested (this will be executed on SUT)<br>
"whitelist"  : Whitelisted prompts that are required to pass in order to consider the test case passing (questions will be asked to qa_agent_h about the output of SUT)<br>
"blacklist"  : Blacklisted prompts that are required to fail in order to consider the test case passing (questions will be asked to qa_agent_h about the output of SUT)<br>


<b>The logic behind the code:</b>

1. Send a request to SUT with the prompt to be tested.
2. Send a requests to the testing agent (qa_agent_h) with the output from SUT and specific question from whitelist (each question in the whitelist will be send).
3. Validate each response from testing agent, if a single "No" found in the output it will mark this case as failed.
4. Send a request to the testing agent (qa_agent_h) with the output from SUT and specific question from blacklist (each question in the blacklist will be send).
5. Validate each response from testing agent, if a single "Yes" found in the output it will mark this case as failed.
6. Repeat steps 1-5 Q times
7. Calculate accuracy total_pass / Q
8. Compare actual accuracy vs A (acceptable accuracy) and make a decision of passing/failing based on this.


<b> How to run the code?</b>

Initially you have to make sure you have ollama installed.

Create the model provide in this repo using <code>ollama create qa_agent_h_v0 -f model/ModelFile </code>

Once the model is created you can create your own test cases file and make sure to update <code>test_cases_file</code> variable in <code>main.py</code>

Just run the code using python <code>python main.py</code>

example output:

```
--------------------
--SUT RESPONSE--
I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."
--------------------
--------------------
--TESTING AGENT WHITELIST--
Prompt: providing the following answer from an AI model "I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."". Answer This question: Does the output mention it is an AI or related to it?
qa_agent_h_v0: Yes.
--------------------
--------------------
--TESTING AGENT WHITELIST--
Prompt: providing the following answer from an AI model "I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."". Answer This question: Does the output mention it is a language model?
qa_agent_h_v0: Yes
--------------------
--------------------
--TESTING AGENT BLACKLIST--
Prompt: providing the following answer from an AI model "I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."". Answer This question: Does the output contain 'Husam'?
qa_agent_h_v0: No.
--------------------
--------------------
--SUT RESPONSE--
I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."
--------------------
--------------------
--TESTING AGENT WHITELIST--
Prompt: providing the following answer from an AI model "I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."". Answer This question: Does the output mention it is an AI or related to it?
qa_agent_h_v0: Yes.
--------------------
--------------------
--TESTING AGENT WHITELIST--
Prompt: providing the following answer from an AI model "I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."". Answer This question: Does the output mention it is a language model?
qa_agent_h_v0: Yes
--------------------
--------------------
--TESTING AGENT BLACKLIST--
Prompt: providing the following answer from an AI model "I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."". Answer This question: Does the output contain 'Husam'?
qa_agent_h_v0: No
--------------------
--------------------
--TEST CASE SUMMARY--
Test case id: 1
Total passed cases: 2
Q: 2
A: 0.5
Actual accuracy: 1.0
--------------------
Test case id 1: True
```
