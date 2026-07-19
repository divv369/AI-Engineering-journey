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
#1st we'll get a text 

from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    phone:int

schema=Ticket.model_json_schema()

response_format={
    "type": "json_object"
}

system_prompt=f"""
Extract the personal information of the customer  strictly based on the schema and give a json output .{schema}
"""

message_system={
    "role": "system" ,
    "content": system_prompt
}



text="Hello My name is Divyansh . I have a gaming laptop . My address is BH10 . MY emails divyansh_2441069@sliet.ac.in .My contact is 6666666666 .My aim is to be the best version of myself "

prompt=f"""This is a ticket . pleases extract the personal information from this {text}"""

message={
    "role":role ,
    "content":prompt
}

messages=[message_system,message]

response=client.chat.completions.create(model=model , messages=messages ,response_format=response_format)

answer=response.choices[0].message.content
print(answer)


#how be will read it ...
import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

##how to pass them
print(ticket.email)
print(ticket.phone)
print(ticket.issue)
print(ticket.name)

#homework - take resume inpdf or word and have hr 
#give  list of things which the hr is requresed adn you
#  have to extract these from resume
#  and match against the hr list and
#  find the percentage of matching the resume to the requirements