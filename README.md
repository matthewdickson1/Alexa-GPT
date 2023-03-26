# Alexa-GPT
Alexa-GPT is an Alexa skill that leverages OpenAI's GPT-3.5 language model to provide users with conversational answers to their questions.

## Prerequisites
- An Amazon Web Services (AWS) account
- An Alexa Developer account
- Python 3.6 or later installed on your local machine
- An OpenAI API key

## Setup
1. Clone the repository.
2. Install necessary packages with pip install -r requirements.txt.
3. Set your OpenAI API key on line 10.
4. Deploy the skill code to AWS Lambda.
5. Set up the Alexa skill using the Amazon Developer Console.

## Usage
Users can interact with the skill by asking Alexa a question, such as "Alexa, ask Chat GPT how Isaac Newton died". Alexa will then use the OpenAI GPT-3.5 language model to generate a response to the user's question.

The skill includes a HelpIntent, which provides users with an example question to ask the skill.
