import ast
import pandas as pd
import numpy as np
import requests
from model1 import TagRecommend
from sklearn.metrics.pairwise import cosine_similarity
import json
from sklearn.feature_extraction.text import TfidfVectorizer

def listToStr(L):
    if type(L) is list:
        str = ''
        for i in L:
            str = str + " " + i
        return str
    else:
        return L


def recommendRepo(inputs):
    tag = TagRecommend(inputs)
    # print(tag)
    url = "https://api.github.com/search/repositories"
    params = {"q": f"language:{tag[0]}",
            "per_page": 100}
        
    response = requests.get(url, params=params)
    d = response.json()
    data = d['items']
    # print(data)
    dataframe = []
    for i in data:
        about = f"{i['language']} {i['description']} {listToStr(i['topics'])}"
        name = i['name']
        ab = [name , about]
        dataframe.append(ab)
    # print(type(inputs))
    df = pd.DataFrame(data=dataframe , columns=["name" , "about"])
    # print(df)

    inputs['language'] = listToStr(inputs["language"])
    inputs['preferedTechstack'] = listToStr(inputs['preferedTechstack'])
    inputs['preferedIssueType'] = listToStr(inputs['preferedIssueType'])
    inputs['intrest'] = listToStr(inputs['intrest'])

    input_feature = inputs['language'] + " " + inputs['description'] + " " + inputs['preferedTechstack'] + " " + inputs['preferedIssueType'] + " " + inputs['intrest']
    # df = df.astype(str)
    vectorizer = TfidfVectorizer(lowercase=True,stop_words=['english'])
    vectorise_data = vectorizer.fit_transform(df['about'])
    Vectorise_input = vectorizer.transform([input_feature])

    similarity = cosine_similarity(vectorise_data, Vectorise_input)[0]
    top_indeces = np.argsort(-similarity)[:10]

    nearest = df.iloc[top_indeces]
    # print(nearest["name"][0])
    return nearest['name'][0]

data = {
    "language": ["HCL", "C++"],
    "topics": ["devops", "automation", "quantum-computing"],
    "description": "SaaS starter kit with Next.js, Prisma and Stripe integration",
    "introduction": "",
    "preferedTechstack": ["Kubernetes", "Q#"],
    "learningGoal": [],
    "intrest":["Cloud Computing", "Cryptography"],
    "preferedIssueType": ["good first issue", "cxbcj"]  
}
repo = recommendRepo(data)
print(repo)