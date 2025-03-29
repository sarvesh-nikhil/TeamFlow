from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from csv_write import write_to_csv
from fastapi.middleware.cors import CORSMiddleware
import csv
from collections import defaultdict
from fastapi.responses import JSONResponse

# nlp : 'ask me' processing
from ml.skill_extraction import extract_skills
from ml.skill_matching import match_skills


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserDetails(BaseModel):
    id: str
    name: str
    email: str
    age: int
    skills: List[str]
    department: str
    designation: str
    yearsofexp: int
    status: str


class SkillsRequest(BaseModel):
    skillsReq: List[str]

class JobDescription(BaseModel):
    description:str

# authentication
class User(BaseModel):
        username: str
        college: str
        password:str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
        access_token: str
        token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None








@app.post('/submit-details/')
def submit_details(details: UserDetails):
    write_to_csv(details.id, details.name, details.email, details.age, details.skills, details.department, details.designation, details.yearsofexp, details.status)
    return {'message': 'User Details Received', 'details': details}



def read_csv():
    user_data = []
    with open('user_details.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            user_id, name, email, age, skills_str, department, designation, yearsofexp, status = row
            skills = [skill.strip() for skill in skills_str.split(',')]
            user_data.append(UserDetails(
                id=user_id, 
                name=name, 
                email=email, 
                age=int(age), 
                skills=skills,
                department=department,
                designation=designation,
                yearsofexp=int(yearsofexp),
                status=status
            ))
    return user_data

@app.get('/get-data/', response_model=List[UserDetails])
def get_data():
    user_data = read_csv()
    return user_data

@app.get('/get-data/{id}', response_model=UserDetails)
def get_data_id(id:str):
    data = read_csv()
    for user in data:
        if user.id == id:
            return user

@app.get("/check-id/{id}")
async def check_id(id: str):
    data = read_csv()
    for user in data:
        if user.id == id:
            return {"exists": True}
    return {"exists": False}


@app.post('/required-skills/')
async def skill_requirements(details: SkillsRequest):
    user_data = read_csv()
    matches = []

    def match_skills(required_skills, employee_skills):
        return len(set(required_skills) & set(employee_skills))

    for user in user_data:
        match_score = match_skills(details.skillsReq, user.skills)
        matches.append((match_score, user))

    # Sort employees by match score in descending order and take the top 5
    top_matches = sorted(matches, key=lambda x: x[0], reverse=True)[:5]

    return [user for score, user in top_matches]


designations = ["architect", "lead architect", "senior engineer", "engineer", "associate", "imagineer"]

@app.get("/designation-counts")
async def get_designation_counts():
    designation_counts = defaultdict(int)
    with open('user_details.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            _, _, _, _, _, _, designation, _, _ = row
            designation_counts[designation.lower()] += 1
    
    result = {designation: designation_counts[designation] for designation in designations}
    return JSONResponse(content=result)

# @app.post("extract-skills/")
# async def extract_skills(job_desc: JobDescription):
#     description_text = job_desc.description
#     required_skills = extract_skills(description_text)
#     user_data = read_csv()
#     matches = match_skills(required_skills, user_data)

@app.post('/extract-skills/')
async def extract_skills_and_match(job_desc: JobDescription):
    try:
        # Extract required skills from job description
        description_text = job_desc.description
        required_skills = extract_skills(description_text)
        user_data = read_csv()

        # Function to calculate match score
        def calculate_match_score(required_skills, employee_skills):
            return len(set(required_skills) & set(employee_skills))

        # Calculate match scores for all users
        matches = [
            (calculate_match_score(required_skills, user.skills), user)
            for user in user_data
        ]

        # Sort users by match score in descending order and take the top 5
        top_matches = sorted(matches, key=lambda x: x[0], reverse=True)[:2]

        # Return only the top 5 matched users
        return [user for score, user in top_matches]
        matches = match_skills(required_skills, user_data)
        # return matches
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
