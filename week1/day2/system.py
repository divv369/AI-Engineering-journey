import os 
from pathlib import Path
from dotenv import load_dotenv 
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key is missing ")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
role="user"
prompt="how can i efficiently finish dsa in 6 months for internship " 

message_system={
    "role": "system" ,
    "content": "you are an highly experieced software development with 20-30 years of experience"
}
message={
    "role":role ,
    "content":prompt
}

messages=[message_system, message]

response=client.chat.completions.create(model=model , messages=messages ,temperature=2)
## print(response) 
answer=response.choices[0].message.content
print(answer)

# notes so 1st error which occured was that i have not saved the file only i have just pasted the cdoe so than error was coming that path was missing after daving it sated working 

# what i did here was i gavve the llm a system role and also i have generated 2 types of responses by altering the temperature .
