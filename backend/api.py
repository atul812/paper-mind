from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import asyncio
import time
import json
import logging
from backend.pipeline import run_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info(f"[PIPELINE_START] query={query}")

    if not query:
        logger.error("[PIPELINE] Empty query")
        return {
            "error": "query is required"
        }

    # cache check
    if query in CACHE:
        cached_data, timestamp = CACHE[query]
        if time.time() - timestamp < CACHE_TTL:
            logger.info(f"[PIPELINE] CACHE_HIT: {query}")
            return {
                "cached": True,
                "data": cached_data
            }

    # run backend pipeline async
    try:
        logger.info(f"[PIPELINE] Starting async pipeline for: {query}")
        pipeline_start = time.time()

        result = await run_pipeline_async(query)

        pipeline_elapsed = time.time() - pipeline_start
        logger.info(f"[PIPELINE] Completed in {pipeline_elapsed:.2f}s")

        result = jsonable_encoder(result)

        logger.info(f"[PIPELINE] Result keys: {list(result.keys())}")
        logger.info(f"[PIPELINE] Data counts:")
        logger.info(f"  - papers: {len(result.get('papers', []))}")
        logger.info(f"  - velocity: {len(result.get('velocity', []))}")
        logger.info(f"  - citation_velocity: {len(result.get('citation_velocity', []))}")
        logger.info(f"  - momentum: {len(result.get('momentum', []))}")
        logger.info(f"  - forecast: {len(result.get('forecast', []))}")
        logger.info(f"  - top_accelerating: {len(result.get('top_accelerating', []))}")
        logger.info(f"  - topics: {len(result.get('topic_map', {}))}")

        # Log first 500 chars of result
        result_str = json.dumps(result, default=str)[:500]
        logger.info(f"[PIPELINE] Response preview: {result_str}")

        # store in cache
        CACHE[query] = (
            result,
            time.time()
        )

        return {
            "cached": False,
            "data": result,
            "elapsed_seconds": pipeline_elapsed,
        }

    except Exception as e:
        logger.error(f"[PIPELINE] ERROR: {str(e)}", exc_info=True)
        return {
            "error": str(e)
        }

