<b>Welcome to qa_agent_h</b>

qa_agent_h is an AI model based on llamma3.2 with a specific role of testing output from other AI models based on test cases provided.

<b>How it works?</b>

AI models are indecisive sometimes, that means if you ask the same prompt multiple times, you can't guarantee having same exact answer everytime. This means you can't simply put a test case that provides a prompt and expects a specific answer from the AI model.
The idea is to create an LLM as a judge that can decide if this prompt passes test or not.

Test_cases/Test_cases_example.json file describes the test cases for specific model
<code>
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
</code>
"SUT"        : The Subject Under Test, which is the model we are currently testing.
"id"         : Test case id
"Q"          : How many times should the same test case repeat
"A"          : Acceptable accuracy of testing (total_pass_attempts / Q must be >= A)
"prompt"     : The prompt to be tested (this will be executed on SUT)
"whitelist"  : Whitelisted prompts that are required to pass in order to consider the test case passing (questions will be asked to qa_agent_h about the output of SUT)
"blacklist"  : Blacklisted prompts that are required to fail in order to consider the test case passing (questions will be asked to qa_agent_h about the output of SUT)
