from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import sqlite3
import os
from typing import Optional, List
from datetime import datetime

DB = os.getenv("FILAHOSPITAL_DB", "./filahospital.db")

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.executescript(open("schema.sql").read())
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="FilaHospital - Protótipo")

class PatientCreate(BaseModel):
    name: str
    dob: Optional[str]
    document: Optional[str]
    contact_phone: Optional[str]

class QueueEntryCreate(BaseModel):
    patient_id: int
    priority: Optional[int] = 3
    notes: Optional[str] = None

class QueueEntry(BaseModel):
    entry_id: int
    unit_id: int
    patient_id: int
    priority: int
    status: str
    created_at: str
    notes: Optional[str]

@app.post("/patients", status_code=201)
def create_patient(p: PatientCreate):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO patients (name, dob, document, contact_phone) VALUES (?, ?, ?, ?)",
                (p.name, p.dob, p.document, p.contact_phone))
    patient_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"patient_id": patient_id}

@app.post("/units/{unit_id}/queue/entries", status_code=201, response_model=QueueEntry)
def enqueue(unit_id: int = Path(...), e: QueueEntryCreate = None):
    if e is None:
        raise HTTPException(status_code=400, detail="Missing body")
    created_at = datetime.utcnow().isoformat() + "Z"
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO queue_entries (unit_id, patient_id, priority, status, created_at, notes) VALUES (?, ?, ?, 'waiting', ?, ?)",
                (unit_id, e.patient_id, e.priority, created_at, e.notes))
    entry_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT entry_id, unit_id, patient_id, priority, status, created_at, notes FROM queue_entries WHERE entry_id = ?", (entry_id,))
    row = cur.fetchone()
    conn.close()
    return {
        "entry_id": row[0],
        "unit_id": row[1],
        "patient_id": row[2],
        "priority": row[3],
        "status": row[4],
        "created_at": row[5],
        "notes": row[6]
    }

@app.get("/units/{unit_id}/queue", response_model=List[QueueEntry])
def list_queue(unit_id: int = Path(...)):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT entry_id, unit_id, patient_id, priority, status, created_at, notes FROM queue_entries WHERE unit_id = ? AND status = 'waiting' ORDER BY priority ASC, created_at ASC", (unit_id,))
    rows = cur.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "entry_id": row[0],
            "unit_id": row[1],
            "patient_id": row[2],
            "priority": row[3],
            "status": row[4],
            "created_at": row[5],
            "notes": row[6]
        })
    return result


@app.get("/health")
def health():
    """Health check: verifica conectividade com DB e existência do arquivo."""
    db_path = DB
    db_exists = False
    db_ok = False
    try:
        db_exists = os.path.exists(db_path)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        conn.close()
        db_ok = True
    except Exception as e:
        db_ok = False
    return {"status": "ok" if db_ok else "fail", "db": {"path": db_path, "exists": db_exists, "ok": db_ok}}
