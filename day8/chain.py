import os 
import time 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API KEY MISSING ")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"

JD="""
    We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
RESUME="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def ask_llm(system_prompt,user_prompt):
    system_msg={
        "role":"user",
        "content": system_prompt
    }

    user_msg={
        "role":"user",
        "content": user_prompt
    }

    messages=[system_msg,user_msg]
    response=client.chat.completions.create(model=model , messages=messages)
    answer=response.choices[0].message.content
    return answer

def step1_res_extract(RESUME):
    system_prompt="""
you are a professional hr assistant . extract the skills from the candidate resume provided . only return the valid
skills information . do not invent any skills by yoursefl 
output format:skills shouydl be seperated by commas and do no t return ay other filler information
"""

    user_prompt=f"""
    extract the skill form the resume 
    {RESUME}
"""
    return ask_llm(system_prompt,user_prompt)

def step2_JD_extract(JD):
    system_prompt="""
you are a professional hr assitant extract the skill sfrom the job description provided 
only return the skills no other information a nd do not invent any new skills
output: skills should be seperated by commas.
    """

    user_prompt=f"""
    extract the skills from the JD: {JD}
"""
    return ask_llm(system_prompt,user_prompt )



def step3_match(candidate,jd):
    print("step3")
    system_prompt="""
    You are a professional HR assistant. compare the skills of candidate and the skills required in the JD and produce a final score between
    1 and 100. also produce a short verdict whther the candidate is a good fit for the role.
    """
    user_prompt=f"""
    Compare and matc h the skills
    JD:
    {jd}
    Candidate:
    {candidate}
    """
    return ask_llm(system_prompt, user_prompt)

candidate=step1_res_extract(RESUME)
print(candidate)
sleep(2)
jd=step2_JD_extract(JD)
print(jd)
sleep(2)
score=step3_match(candidate,jd)
print(score)


