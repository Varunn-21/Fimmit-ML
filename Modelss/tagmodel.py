import ast
import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer



def listToStr(l):
    if isinstance(l,str):
        l = ast.literal_eval(l)
    s = ""
    for i in l:
        s = s + " " + i
    return s


def TagRecommend(input):
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir,'Updated_data.csv')
    data_csv = pd.read_csv(file_path)
    datac = data_csv['mixed'] 

    input['language'] = listToStr(input["language"])
    input["topics"] = listToStr(input['topics'])
    input['preferedTechstack'] = listToStr(input['preferedTechstack'])
    input['preferedIssueType'] = listToStr(input['preferedIssueType'])
    input['intrest'] = listToStr(input['intrest'])



    input_feature = input['language'] + " " + input['topics'] + " " + input['description'] + " " + input['preferedTechstack'] + " " + input['preferedIssueType'] + " " + input['intrest']

    vectorizer = TfidfVectorizer(lowercase=True,stop_words=['english'])
    vectorise_data = vectorizer.fit_transform(datac)
    Vectorise_input = vectorizer.transform([input_feature])

    # print(vectorise_data.shape)
    # print(Vectorise_input.shape)
    # print(Vectorise_input)
    # print(vectorise_data)

    similarity = cosine_similarity(Vectorise_input, vectorise_data)[0]
    top_indeces = np.argsort(-similarity)[:5]


    nearest = data_csv.iloc[top_indeces]
    best = nearest.iloc[0]

    arr = str(best['recommended_tags']).strip().split()
    tags = [best['recommended_language']] + arr[:3] + [best['recommended_issue_type']]
    return tags



    #print(tags)





# data = {
#     "language": ["HCL", "C++"],
#     "topics": ["devops", "automation", "quantum-computing"],
#     "description": "SaaS starter kit with Next.js, Prisma and Stripe integration",
#     "introduction": "",
#     "preferedTechstack": ["Kubernetes", "Q#"],
#     "learningGoal": [],
#     "intrest":["Cloud Computing", "Cryptography"],
#     "preferedIssueType": ["good first issue", "cxbcj"]  
# }
# tag = TagRecommend(data)
# print(tag)