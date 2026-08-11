import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api key missing ")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"

# step1 =create a knowledge base so that we can retireve the data from it 
knowledge_base={
    "age": "divyansh age is 20" ,
    "divyansh" : "Divyansh is a 3rd year student of SLIET" 
}
# prbls - very rigid software , if spelling msitake then no vlaid output .

def retrieve(question):
    question=question.lower()
    if "age" in question:
        return knowledge_base["age"]
    elif "divyansh" in question:
        return knowledge_base["divyansh"]
    else :return None


def ask_llm(question):
    context=retrieve(question)

    sys_prompt=f"""answer in one line only,and answer only based on the context. context:{context} """
    system_message={
        "role":"user",
        "content": sys_prompt
    }
    message={
        "role":"user" ,
        "content":question
    }
    messages=[system_message,message] 
    response=client.chat.completions.create(model=model, messages=messages)
    answer=response.choices[0].message.content
    return answer

question="Who is divyansh  form sliet colege?"
print(ask_llm(question))