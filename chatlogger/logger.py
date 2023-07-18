import os 
import json 
import threading
from datetime import datetime

class ChatLogger:
    def __init__(self, openai_create_function, file_path = None):
        if file_path is None:
            self.file_path = f"chatlog_{datetime.now().strftime('%Y%m%d')}.jsonl"
        else:
            self.file_path = file_path
        self.openai_create_function = openai_create_function

        #Create the file if it does not exist
        f = open(self.file_path, "a")
        f.close()

        #Extract the format of the file
        self.format = self.file_path.split(".")[-1]

    def log(self, chat_prompt, chat_response):
        #temporarily log all the chats, including the ones that are already in the list
        chat_data = {
            "id": chat_response["id"],
            "conversations": [], 
            "quality": 0
        }
        chat_data["conversations"] += chat_prompt 
        chat_data["conversations"].append(chat_response["choices"][0]["message"])

        #jsonl saves memory
        if self.format == "jsonl":
            with open(self.file_path, "a") as f:
                f.write(json.dumps(chat_data) + "\n")
            return

        #Save the chat to the json file 
        with open(self.file_path, 'r') as f:
            json_list = json.load(f)

        json_list.append(chat_data)
        with open(self.file_path, 'w') as f: 
            json.dump(json_list, f, indent = 4)

        return


    def log_stream(self, *args, **kwargs):
        temp_response = {
            "id":None, 
            "choices": [
                {
                    "message": {
                        "role":"assistant",
                        "content":""
                    }
                }
            ]
        }
        openai_response = self.openai_create_function(*args, **kwargs)
        for chunk in openai_response:
            if temp_response["id"] is None:
                temp_response["id"] = chunk["id"]
            if "content" in chunk["choices"][0]["delta"].keys():
                temp_response["choices"][0]["message"]["content"] += chunk["choices"][0]["delta"]["content"]
            yield chunk

        #Log the response
        threading.Thread(target=self.log, args=(kwargs.get("messages"), temp_response)).start()

    def log_chat(self, *args, **kwargs):
        openai_response = self.openai_create_function(*args, **kwargs)
        threading.Thread(target = self.log, args=(kwargs.get("messages"), openai_response)).start()
        return openai_response

    def __call__(self, *args, **kwargs):
        stream = kwargs.get("stream", False)
        return self.log_stream(*args, **kwargs) if stream else self.log_chat(*args, **kwargs)
