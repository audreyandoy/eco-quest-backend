"""
For now this is experimenting with ChatGPT code.
Ensure OPENAI_API_KEY environmental variable is set with the API Key provided by OpenAI

Prompt-Engineering
------------------
Typically, a conversation is formatted with a system message first, followed by alternating user and assistant messages.
The system message helps set the behavior of the assistant.
The user messages provide requests or comments for the assistant to respond to.
Assistant messages store previous assistant responses, but can also be written by you to give examples of desired behavior.

Model temperature setting: Lower values for temperature result in more consistent outputs, while higher values generate
more diverse and creative results. Select a temperature value based on the desired trade-off between coherence and
creativity for your specific application.
"""

import os
import json
import time
import openai
import requests
from transformers import AutoTokenizer
from .models import Profile, EcoTransport

NEW_CHATGPT = False

#  App house-keeping
current_time = time.time()
output_folder = "./debug"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Select Model
# models = openai.Model.list()
MODEL = "gpt-4-0314"  # "gpt-3.5-turbo"  # "gpt2"

# Stored Prompts
EXAMPLE_USER_DATA = {  # Example User Data
    "challenge": "Travel More Sustainably",  # "Eat More Plant-Based Food"
    "activities": ["walked to work", "took bus to show", "walked to grocery"],
}

EXAMPLE_PREVIOUS_CONTENT = None

SYSTEM_TEXT = """As a sustainability expert, you will be advising our EcoQuest app user how to improve their habits
for living more sustainably based on their usage data and topic provided.  Please provide only the text response 
in 200 words or less, appropriate for middle school, and without greetings.  
"""

PROMPT_TEXT = f"""Provide one of the following based on the User Information (1) background educational material,
(2) a tip to the user on how to increase their good activity, or (3) how to add add new sustainability activities related
to the challenge. User Information: 
"""


# Utility Functions
def estimate_tokens(text, model_name="gpt2"):
    """
    Function to estimate the number of tokens used in the message.
    This doesn't seem super accurate...TBD
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)


# # Estimate tokens
# for i, msg in enumerate(messages):
#     estimated_tokens = estimate_tokens(msg["content"])
#     print(f"{msg['role']} message {i} est tokens:", estimated_tokens)

# Database call functions
# TODO #1 need one to retrieve user data from database and pre-process to reduce tokens
# TODO #2 potentially save response to database to keep for seeding next prompt/speeding up service
# TODO #3 function to get last saved prompt
# TODO #4 how to handle when text is marked "read" and given points?  Per "quest".


# Function to call GPT and generate content based on the conversation context and user profile.
def generate_custom_content(
    user_info=EXAMPLE_USER_DATA,
    previous_content=EXAMPLE_PREVIOUS_CONTENT,
    max_tokens=200,
    save_output=False,
    display_output=False,
):
    """
    Generate custom content for a user based on their activity, readings, and preferences.

    :param user_info: dict, containing user's data such as age, sex, location and previous app usage summary.
    :param previous_content: str, content that the user has read or interacted with in the past.
    :param max_tokens: int, the maximum length of the generated content.
    :return: str, custom-generated content for the user.
    """

    # Construct the conversation history or context from previous_content and user_info.
    # This part is highly dependent on how your application stores and manages user data.
    prompt = PROMPT_TEXT + str(user_info)
    if previous_content is not None:
        prompt += f"User's previous readings include: {previous_content}."

    messages = [
        {"role": "system", "content": SYSTEM_TEXT},
        {"role": "user", "content": prompt},
    ]

    # Get ChatGPT Response
    completion = openai.ChatCompletion.create(
        model=MODEL, messages=messages, max_tokens=max_tokens
    )

    # Extract the text from the GPT-3 response
    text = completion.choices[0].message.content.strip()

    if display_output:
        print("Selected model" + MODEL + "\n")

        print("CHATGPT submitted prompts")
        print(messages)
        print()

        print(completion.choices[0].message)
        print(completion.usage)

    if save_output:
        with open(
            os.path.join(output_folder, f"chatgpt_result_{current_time}.txt"), "w"
        ) as file:
            file.write(completion.choices[0].message.content)

        with open(
            os.path.join(output_folder, f"chatgpt_full_result_{current_time}.json"), "w"
        ) as file:
            file.write(json.dumps(completion, indent=4))

    return text


if __name__ == "__main__":
    if NEW_CHATGPT:
        generate_custom_content(save_output=True, display_output=True)

    print(Profile.objects.all())
    print(EcoTransport.objects.all())