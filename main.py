import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document, get_documents
from schemas import Course, Instructor, Enrollment

app = FastAPI(title="Academy API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Academy API is running"}

# Public content endpoints

@app.get("/api/courses", response_model=List[Course])
def list_courses():
    try:
        docs = get_documents("course", limit=50)
        # Coerce _id and timestamps out for response model compliance
        clean = []
        for d in docs:
            d.pop("_id", None)
            d.pop("created_at", None)
            d.pop("updated_at", None)
            clean.append(d)
        return clean
    except Exception as e:
        # If DB not configured, return a few sample records to keep site functional
        return [
            {
                "title": "Full-Stack Web Development",
                "summary": "Learn React, FastAPI, databases, and deployment.",
                "duration_weeks": 12,
                "level": "Beginner",
                "tags": ["react", "python", "api"],
                "thumbnail": None,
            },
            {
                "title": "Data Science Fundamentals",
                "summary": "Statistics, Python, Pandas, and visualization.",
                "duration_weeks": 10,
                "level": "Intermediate",
                "tags": ["pandas", "numpy", "viz"],
                "thumbnail": None,
            },
        ]

@app.get("/api/instructors", response_model=List[Instructor])
def list_instructors():
    try:
        docs = get_documents("instructor", limit=50)
        clean = []
        for d in docs:
            d.pop("_id", None)
            d.pop("created_at", None)
            d.pop("updated_at", None)
            clean.append(d)
        return clean
    except Exception:
        return [
            {
                "name": "Alex Rivera",
                "title": "Senior Software Engineer",
                "bio": "10+ years building scalable web apps.",
                "avatar": None,
                "specialties": ["React", "FastAPI", "DevOps"],
            },
            {
                "name": "Maya Chen",
                "title": "Data Scientist",
                "bio": "Data wrangler and storyteller.",
                "avatar": None,
                "specialties": ["Pandas", "ML", "Visualization"],
            },
        ]

# Enrollment submission

@app.post("/api/enroll")
def apply_enrollment(payload: Enrollment):
    try:
        create_document("enrollment", payload)
        return {"ok": True, "message": "Application received. We'll reach out soon!"}
    except Exception:
        # Still accept in no-DB mode to not block the UX
        return {"ok": True, "message": "Application received! (temporary mode)"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
