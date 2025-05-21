#model is too big to upload to github, 5gb is the limit. 
#Before running this script, download the model from gpt4all. 
# then call the file path from whre you saved it like I did above in the below line:
# model_path = r"C:\Users\zachary.daher\AppData\Local\nomic.ai\GPT4All" THIS FILE PATH IS SPECIFIC TO MY COMPUTER, YOU MUST CHANGE IT TO YOURS

from gpt4all import GPT4All

model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model_path = r"C:\Users\zachary.daher\AppData\Local\nomic.ai\GPT4All"

with GPT4All(model_name, model_path=model_path) as model:
    response = model.generate(prompt="This is a test case.")
    print(response)



