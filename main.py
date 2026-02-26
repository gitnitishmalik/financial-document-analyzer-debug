import os
import uuid
import asyncio
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from crewai import Crew, Process

from agents import financial_analyst
from tasks import analyze_task 

app = FastAPI(title="Theatrical Financial Analyzer")

class AnalysisResult(BaseModel):
    status: str
    file_name: str
    analysis_summary: str

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_endpoint(
    file: UploadFile = File(...),
    query: str = Form("Analyze for investment insights")
):
    file_id = str(uuid.uuid4())
    data_dir = Path("temp_uploads")
    data_dir.mkdir(exist_ok=True)

    file_path = (data_dir / f"{file_id}_{file.filename}").absolute()
    safe_path = file_path.as_posix()

    try:
        # Save the file locally
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Initialize Crew with the Task OBJECT
        crew = Crew(
            agents=[financial_analyst],
            tasks=[analyze_task], 
            process=Process.sequential
        )

        # Kickoff with BOTH variables required by the agent and task
        result = await asyncio.to_thread(
            crew.kickoff,
            inputs={"query": query, "file_path": safe_path}
        )

        return {
            "status": "success",
            "file_name": file.filename,
            "analysis_summary": str(result)
        }

    except Exception as e:
        return {"status": "error", "file_name": file.filename, "analysis_summary": str(e)}
    finally:
        if file_path.exists():
            os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)