import ast
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer


BASE_DIR = Path(__file__).resolve().parent
# Vectorizor = joblib.load(BASE_DIR/"tfidf_vectorizer.joblib")
data = pd.read_csv(BASE_DIR/"Updated_data.csv")

def listToStr(l):
    if isinstance(l,str):
        l = ast.literal_eval(l)
    s = ""
    for i in l:
        s = s + " " + i
    return s


def TagRecommend(input):
    input['language'] = listToStr(input["language"])
    input["topics"] = listToStr(input['topics'])
    input['preferedTechstack'] = listToStr(input['preferedTechstack'])
    input['preferedIssueType'] = listToStr(input['preferedIssueType'])
    input['intrest'] = listToStr(input['intrest'])



    input_feature = input['language'] + " " + input['topics'] + " " + input['description'] + " " + input['preferedTechstack'] + " " + input['preferedIssueType'] + " " + input['intrest']

    vectorizer = TfidfVectorizer()
    D = vectorizer.fit_transform(data['mixed']).toarray()
    Vectorise_input = vectorizer.fit_transform([input_feature]).toarray()
    print(Vectorise_input)
    distances = pairwise_distances(Vectorise_input, D, metric="cosine")[0]

    # Get top 5 nearest queries
    nearest_indices = np.argsort(distances)[:5]
    nearest = data.iloc[nearest_indices]

    print(nearest)







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
TagRecommend(data)