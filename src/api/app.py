from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any

app = FastAPI(
    title="Text-to-SQL API",
    description="Convert natural language to SQL queries",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


class SQLResponse(BaseModel):
    question: str
    sql: str
    success: bool
    result: Optional[List[Any]] = None
    error: Optional[str] = None


@app.get("/")
def root():
    return {"status": "ok", "service": "text-to-sql"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/query", response_model=SQLResponse)
def query(request: QuestionRequest):
    from src.sql.generator import generate_sql
    from src.sql.executor import execute_sql
    
    # Generate SQL
    sql = generate_sql(request.question)
    
    # Execute
    success, result, error = execute_sql(sql)
    
    return SQLResponse(
        question=request.question,
        sql=sql,
        success=success,
        result=result.to_dict(orient="records") if success and result is not None else None,
        error=error
    )
