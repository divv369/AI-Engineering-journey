# step 1 imports and enviroment 
import os 
from dotenv import load_dotenv
from qdrant_client import QdrantClient 
from qdrant_client.models import Distance, VectorParams , PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()
#load variables from env 
QDRANT_URL= os.getenv("QDRANT_URL")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
GROQ_API_KEY= os.getenv("GROQ_API_KEY")

# STEP 2 CONNECT T0 QDRANT

client =QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)
print("Connected to Qdrant Cloud")

#step 3 create Qdrant collection 

COLLECTION_NAME="knowledge"
EMBEDDING_SIZE=384

# DELET collection it it already exist 
if client.collection_exists(COLLECTION_NAME):
    print(f"Deleting existitng collection:{COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)
    
    
#create collection 
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=EMBEDDING_SIZE,
        distance=Distance.COSINE,
    ),
)

print(f"Created collection :{COLLECTION_NAME}")
print(f"vector size: {EMBEDDING_SIZE}")
print("Distance:COSINE")

#STEP 4 LOAD OUR KNOWLEDGE

with open("knowledge.txt" , "r" ,encoding="utf-8") as f:
    documents=[
        line.strip()
        for line in f
        if line.strip()]
    
print(f"Loaded {len(documents)} documents")

#step 5 create embeddings

print("Loading embedding model... ")
model =SentenceTransformer("all-MiniLM-L6-v2") #384

print("embedding model ready! ")

embeddings=model.encode(documents)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")

# step 6- create qdrant points

points=[]
for i, embedding in enumerate(embeddings):
    point=PointStruct(
        id=i +1 ,
        vector=embedding.tolist(),
        payload={
            "text":documents[i]
        }
    )
    points.append(point)
    
    #step7 upload to qdrant 
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)
print(f"Uploaded {len(points)} documents to Qdrant!")

#step 8 SEARCH QDRANT 

def search(query, top_k=3):
    query_vector=model.encode(query).tolist()
    
    results=client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k, 
        with_payload=True,
        
    ).points
    
    return results




#step 9 test search
query ="How  many vacation days do i get?"
results=search(query,top_k=3)
print("\nSearch results:")

for result in results:
    print(f"score:{result.score:.3f}")
    print(result.payload["text"])
    print()
    

#step 10 connmect to groq

groq_client=Groq(
    api_key=GROQ_API_KEY
    
)
#STEP 11 ASK THE LLM 
def ask_llm(question,context):
    prompt=f""" 
    answer the4 question using the given information below
    context:{context}
    question:{question}
    if the answer is not present in the context ,say "i dont know based on the 
    provided information."
    """
    response=groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role":"user",
                "content":prompt
                
                
            }
        ]
    )
    
    return response.choices[0].message.content

#step 12 complete rag pipeline

question="how many vacation do i get ?"

result=search(question,top_k=3)


context="\n".join(
    result.payload["text"]
    for result in results
)

answer=ask_llm(question,context)

print("\nFinal Answer:")
print(answer)
