from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

class Task(BaseModel):
    title: str
    status: str = "pending"
    time: str = ""

class TaskUpdate(BaseModel):
    status: str
    time: str

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/tasks")
def create_task(task: Task, uid: str = Depends(verify_token)):
    doc_ref = db.collection("users").document(uid).collection("tasks").document()
    doc_ref.set({"title": task.title, "status": task.status, "time": task.time})
    return {"id": doc_ref.id, "title": task.title, "status": task.status, "time": task.time}

@app.get("/tasks")
def get_tasks(uid: str = Depends(verify_token)):
    tasks_ref = db.collection("users").document(uid).collection("tasks").stream()
    tasks = [{"id": task.id, **task.to_dict()} for task in tasks_ref]
    return {"tasks": tasks}

@app.put("/tasks/{task_id}")
def update_task(task_id: str, task_update: TaskUpdate, uid: str = Depends(verify_token)):
    doc_ref = db.collection("users").document(uid).collection("tasks").document(task_id)
    doc_ref.update({
        "status": task_update.status,
        "time": task_update.time
    })
    return {"message": "Cập nhật thành công"}