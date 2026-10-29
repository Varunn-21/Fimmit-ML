# GDG-Group-task-ML
 
A FastAPI service that powers the ML side of **Fimmit**, a platform that helps people find open-source projects to contribute to. Given a user's profile (languages, interests, preferred stack and issue type), the API:
 
1. **Model 1** recommends GitHub **tags** (language, topics, issue type) to search with.
2. **Model 2** uses those tags to find and rank the **top 10 open-source repositories** from GitHub that best match the user.
**Live API:** [gdg-group-task-ml.onrender.com](https://gdg-group-task-ml.onrender.com)
**Interactive docs:** [gdg-group-task-ml.onrender.com/docs](https://gdg-group-task-ml.onrender.com/docs)
3. Frontenc Link : https://team-task-frontend-henna.vercel.app/
---
 
## Features
 
- Two-stage recommendation pipeline: tags first, repositories second
- TF-IDF vectorisation + cosine similarity (scikit-learn), no heavy model files needed
- Live repository candidates pulled from the GitHub Search API
- Request validation with Pydantic and auto-generated Swagger docs
---
 
## Project Structure
 
```
GDG-Group-task-ML/
├── app.py                      # FastAPI app and routes (/, /tags, /repo)
├── Modelss/
│   ├── tagmodel.py             # Model 1: TagRecommend (tag recommendation)
│   ├── repomodel.py            # Model 2: recommendRepo (repository ranking)
│   ├── dataa.csv               # 4,000 user-profile -> recommendation examples
│   ├── Updated_data.csv        # dataa.csv with a combined text column ("mixed") used by Model 1
│   └── textPreprocess.ipynb    # Text preprocessing notebook
├── Creating Data/
│   ├── PrepareData.ipynb       # Collects repositories from the GitHub API
│   └── data.csv                # Collected repository data (name, description, language, age, topics)
├── requirements.txt
└── .gitignore
```
 
---
 
## How It Works
 
### Model 1: Tag recommendation (`/tags`)
 
1. The user's languages, topics, repo description, preferred tech stack, preferred issue types and interests are joined into one text string.
2. That string and the `mixed` column of `Updated_data.csv` are converted to TF-IDF vectors.
3. Cosine similarity finds the most similar profile in the dataset.
4. The recommended tags of that closest match are returned: **language, three topic tags, and an issue type**.
### Model 2: Repository recommendation (`/repo`)
 
1. Model 1 is run to get the recommended language and topic.
2. The GitHub Search API is queried for up to 100 repositories matching `language:<tag> topic:<tag> stars:>500`.
3. Each candidate is described by its language, description and topics, vectorised with TF-IDF, and compared against the user's profile with cosine similarity.
4. The names of the **top 10** most similar repositories are returned.
---
 
## Tech Stack
 
| Area | Tools |
|------|-------|
| Language | Python |
| API | FastAPI, Uvicorn, Pydantic |
| ML / Data | scikit-learn (TF-IDF, cosine similarity), pandas, NumPy |
| Data source | GitHub REST API (via `requests`) |
 
---
 
## Getting Started
 
### 1. Clone the repository
 
```bash
git clone https://github.com/Varunn-21/GDG-Group-task-ML.git
cd GDG-Group-task-ML
```
 
### 2. Create a virtual environment
 
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```
 
### 3. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Run the server
 
```bash
uvicorn app:app --reload
```
 
The API runs at `http://127.0.0.1:8000` and the docs at `http://127.0.0.1:8000/docs`.
 
---
 
## API Reference
 
### `GET /`
 
Returns a short description of the API and its two models.
 
### Request body (for `POST /tags` and `POST /repo`)
 
| Field | Type | Description |
|-------|------|-------------|
| `language` | `List[str]` | Languages the user knows |
| `topics` | `List[str]` | Topics the user works with |
| `description` | `str` | Description of the user's repositories |
| `introduction` | `str` | Short introduction of the user |
| `preferedTechstack` | `List[str]` | Preferred tech stack |
| `learningGoal` | `List[str]` | Learning goals |
| `intrest` | `List[str]` | Interests |
| `preferedIssueType` | `List[str]` | Preferred issue types |
 
> Field names (`preferedTechstack`, `intrest`, `preferedIssueType`) are spelled exactly as the API expects.
 
**Example**
 
```json
{
  "language": ["Python", "JavaScript"],
  "topics": ["machine-learning", "web"],
  "description": "ML projects and a small FastAPI backend",
  "introduction": "BTech student interested in ML and open source",
  "preferedTechstack": ["Python", "FastAPI"],
  "learningGoal": ["Deep Learning", "Deployment"],
  "intrest": ["NLP", "Data Science"],
  "preferedIssueType": ["good first issue", "documentation"]
}
```
 
### `POST /tags`
 
Returns recommended search tags.
 
```bash
curl -X POST "https://gdg-group-task-ml.onrender.com/tags" \
  -H "Content-Type: application/json" \
  -d @request.json
```
 
**Response shape**
 
```json
{
  "Tags": ["<language>", "<topic 1>", "<topic 2>", "<topic 3>", "<issue type>"]
}
```
 
### `POST /repo`
 
Returns the top 10 recommended repositories (by name) for the same input.
 
**Response shape**
 
```json
{
  "Repo": ["repo-name-1", "repo-name-2", "...", "repo-name-10"]
}
```
 
---
 
## Data
 
- **`Creating Data/`**: `PrepareData.ipynb` collects repository metadata (description, name, language, age, topics) from the GitHub Search API into `data.csv`.
- **`Modelss/dataa.csv`**: 4,000 examples mapping a user profile (languages, topics, description, tech stack, issue types, interests) to a recommended language, issue type and tags.
- **`Modelss/Updated_data.csv`**: the same examples with the profile fields merged into a single `mixed` text column, which Model 1 vectorises.
---
 
## Notes
 
- Model 2 calls the GitHub Search API without authentication, so it is subject to GitHub's unauthenticated rate limits.
- The first request after a period of inactivity may be slow on free hosting tiers.
---
 
## Author
 
**Varun Kumar**: [@Varunn-21](https://github.com/Varunn-21)
 
Built as a GDG group task for Fimmit.
