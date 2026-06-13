from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time
from backend.pipeline import run_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# simple in memory cache

CACHE = {}
CACHE_TTL = 60 * 30  # 30 minutes

class QueryRequest(BaseModel):
    query: str

# async wrapper
async def run_pipeline_async(query: str):

    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        None,
        run_pipeline,
        query
    )

    return result

# health check
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# main pipeline endpoint (with cache + async)

@app.post("/api/pipeline")
async def pipeline(request: QueryRequest):

    query = request.query.strip().lower()
    if not query:
        return {
            "error": "query is required"
        }

    # cache check
    if query in CACHE:
        cached_data, timestamp = CACHE[query]
        if time.time() - timestamp < CACHE_TTL:
            return {
                "cached": True,
                "data": cached_data
            }

    # run backend pipeline async
    try:
        result = await run_pipeline_async(query)
        # store in cache
        CACHE[query] = (
            result,
            time.time()
        )
        return {
            "cached": False,
            "data": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }