import sys 
sys.path.append("..")
import os
import openai 
from chatlogger import ChatLogger

openai.api_key = "YOUR_API_KEY"
openai.ChatCompletion.create = ChatLogger(openai.ChatCompletion.create, file_path = "chatlog.jsonl")

response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {
            "role": "user",
            "content": "Hello, who are you?"
        }
    ],
    stream = True
)

for chunk in response:
    try:
        print(chunk["choices"][0]["message"]["content"])
    except: 
        pass 

#Another test with normal response
response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {
            "role": "user",
            "content": "Hello, who are you?"
        }
    ]
)
print(response["choices"][0]["message"]["content"])