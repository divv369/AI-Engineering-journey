import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api missing")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"

def llm_ans(prompt):
    message={
        "role":"user",
        "content":prompt
    }
    messages=[message]
    response=client.chat.completions.create(model=model ,messages=messages)
    ans=response.choices[0].message.content
    return ans;



bad_prompt=""""
1.ROLE:
YOU ARE a support assistant at a mobile/laptop company 
2. TASK:
you have to clarify the issue .
3.CONSTRSIN:
you ahve to select from these 3 categories only :
technical, return , billing  .

4. output format = output only in one word 

5. example my laptop is not working is a technical issue

6. fallback: if something irrelevant is asked then return other.
this is a user complain: 
my girlfirend leave me
.
"""

print(llm_ans(bad_prompt))