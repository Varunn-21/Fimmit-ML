from fastapi import FastAPI
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field
from typing import List , Annotated
from Modelss.tagmodel import TagRecommend 
from Modelss.repomodel import recommendRepo 

app = FastAPI()

class Inputs(BaseModel):
    language: Annotated[List[str] , Field(description="Enter the list of all the languages user know")]
    topics: Annotated[List[str] , Field(description="Enter the list of all the topics")]
    description: Annotated[str , Field(description="Enter the list of repo Description")]
    introduction: Annotated[str , Field(description="Enter the Introduction of user")]
    preferedTechstack: Annotated[List[str] , Field(description="Enter the list of Preferred TechStack")]
    learningGoal: Annotated[List[str] , Field(description="Enter the list of Learning goal")]
    intrest: Annotated[List[str] , Field(description="Enter the list of Intrest")]
    preferedIssueType: Annotated[List[str] , Field(description="Enter the list of Preferred Issue Type")]



    


@app.get("/")
def into():
    return JSONResponse(content={
        "Message":"This API is for ML model made by Varun Kuamr for Fimmit",
        "Model 1" : "It recommend Tags to search open source repository",
        "Model 2" : "It recommend Top 10 open source Repo Based on Model 1 tags"
    })


@app.post("/tags")
def tags(Inputs : Inputs):
    tag = TagRecommend(Inputs.model_dump())
    return JSONResponse(
        status_code=200,
        content={
           "Tags" : tag
        })


@app.post("/repo")
def tags(Inputs : Inputs):
    repo = recommendRepo(Inputs.model_dump())
    return JSONResponse(
        status_code=200,
        content={
           "Repo" : repo
        })
