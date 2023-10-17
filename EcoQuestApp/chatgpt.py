"""
For now this is experimenting with ChatGPT code.

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
from transformers import AutoTokenizer

# Ensure OPENAI_API_KEY environmental variable is set with the API Key provided by OpenAI

print(openai.api_key)
current_time = time.time()
output_folder = "./debug"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# list models
models = openai.Model.list()
# # print the first model's id
# print("\nAvailable models:")
# for model in models.data:
#     print(model.id)

# Set model
MODEL = "gpt-4-0314" #"gpt-3.5-turbo"  # "gpt2"
print("Selected model" + MODEL + "\n")

def estimate_tokens(text, model_name="gpt2"):
    """
    Function to estimate the number of tokens used in the message.
    This doesn't seem super accurate...TBD
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)



max_words = 200

user_data = {
    "challenge": "Travel More Sustainably",  # "Eat More Plant-Based Food"
    "activities": ["walked to work", "took bus to show", "walked to grocery"],
}


SYSTEM_TEXT = """As a sustainability expert, you will be advising our EcoQuest app user how to improve their habits
for living more sustainably based on their usage data and topic provided.  Please provide only the text response 
in 200 words or less, appropriate for middle school, and without greetings.  
"""

PROMPT_TEXT = f"""Provide please provide one of the following based on the User Information (1) background educational material,
(2) a tip to the user on how to increase their good activity, or (3) how to add add new sustainability activities related
to the challenge. User Information: 
"""

messages = [
    {"role": "system", "content": SYSTEM_TEXT},
    {"role": "user", "content": PROMPT_TEXT + str(user_data)}
  ]

print("CHATGPT submitted prompts")
print(messages)
print()

# Estimate tokens
for i, msg in enumerate(messages):
    estimated_tokens = estimate_tokens(msg["content"])
    print(f"{msg['role']} message {i} est tokens:", estimated_tokens)

# Get ChatGPT Response
completion = openai.ChatCompletion.create(
  model=MODEL,
  messages=messages
)

print(completion.choices[0].message)
print(completion.usage)

with open(os.path.join(output_folder, f"chatgpt_result_{current_time}.txt"), "w") as file:
    file.write(completion.choices[0].message.content)

with open(os.path.join(output_folder, f"chatgpt_full_result_{current_time}.json"), "w") as file:
    file.write(json.dumps(completion, indent=4))
