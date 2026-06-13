from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add project root to path
project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, project_root)

from graph.workflow import graph

app = FastAPI(
    title="NetOps RCA System",
    description="Multi-Agent Network Root Cause Analysis System",
    version="1.0"
)


class AlertRequest(BaseModel):
    alert: str


@app.get("/")
def home():
    return {
        "message": "NetOps RCA API Running"
    }


@app.post("/analyze")
def analyze_alert(request: AlertRequest):

    try:

        result = graph.invoke(
            {
                "alert": request.alert
            }
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )