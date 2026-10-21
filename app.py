from fastapi import FastAPI
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field
from typing import List , Annotated

app = FastAPI()

class Inputs(BaseModel):
    language: Annotated[List[str] , Field(description="Enter the list of all the languages user know")]
    topics: Annotated[List[str] , Field(description="Enter the list of all the topics")]
    description: Annotated[List[str] , Field(description="Enter the list of repo Description")]
    introduction: Annotated[str , Field(description="Enter the Introduction of user")]
    preferedTechstack: Annotated[List[str] , Field(description="Enter the list of Preferred TechStack")]
    learningGoal: Annotated[List[str] , Field(description="Enter the list of Learning goal")]
    intrest: Annotated[List[str] , Field(description="Enter the list of Intrest")]
    preferedIssueType: Annotated[List[str] , Field(description="Enter the list of Preferred Issue Type")]



    


@app.get("/")
def into():
    return JSONResponse(content={
        "Message":"This API is for ML model made by Varun Kuamr for Fimmit",
        "Model 1" : "It recommend Tags to search open source repository"
    })

@app.get("/tags")
def tags(Inputs : Inputs):
    
