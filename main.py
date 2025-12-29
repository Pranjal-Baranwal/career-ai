from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
print("API KEY LOADED:", bool(os.getenv("GOOGLE_API_KEY")))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    timeout=30,
    max_retries=1
)

parser = StrOutputParser()

prompt = PromptTemplate(
    template="""
You are a professional career guidance counselor.

Education type: {education_type}
Age / Grade group: {age_group}
Current education level: {current_education}
Technical skills: {technical_skills}
Soft skills: {soft_skills}
Hobbies and interests: {hobbies}
Preferred industry: {industry}
Job expectations: {expectation}

Provide:
1. 3–5 recommended career options
2. Why each option suits the user
3. Skills to improve
4. Learning roadmap
""",
    input_variables=[
        "education_type",
        "age_group",
        "current_education",
        "technical_skills",
        "soft_skills",
        "hobbies",
        "industry",
        "expectation"
    ]
)

chain = prompt | model | parser


class CareerRequest(BaseModel):
    education_type: str
    age_group: str
    current_education: str
    technical_skills: str
    soft_skills: str
    hobbies: str
    industry: str
    expectation: str


@app.post("/recommend")
def recommend(data: CareerRequest):
    try:
        result = chain.invoke(data.dict())
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}