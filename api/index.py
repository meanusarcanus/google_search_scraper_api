"""
FastAPI Serverless Handler for Google SERP & Search Intelligence Extractor API
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add parent directory to sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from core.serp_scraper import scrape_google_serp

app = FastAPI(
    title="Google SERP & Search Intelligence Extractor API",
    description="Extract organic search rankings, sponsored ads, and People Also Ask queries with custom geolocation and page depth controls.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# Pydantic Schemas
# ==============================================================================
class SearchRequest(BaseModel):
    search_queries: List[str] = Field(..., description="List of search queries or topics to query Google SERPs")
    page_depth: Optional[int] = Field(default=1, ge=1, le=5, description="Number of SERP pagination pages to extract per query")
    country_code: Optional[str] = Field(default="us", description="Two-letter ISO country code for geo-location (e.g. us, ph, uk, th)")
    language_code: Optional[str] = Field(default="en", description="Two-letter language code (e.g. en, es, fr, th)")
    include_paa: Optional[bool] = Field(default=True, description="Extract People Also Ask (PAA) question blocks")
    include_paid_ads: Optional[bool] = Field(default=True, description="Extract sponsored PPC Google Ads")

class OrganicItem(BaseModel):
    position: int
    title: str
    url: str
    domain: str
    snippet: str
    sitelinks: Optional[List[Dict[str, str]]] = None

class SearchResponseItem(BaseModel):
    search_query: str
    country_code: str
    language_code: str
    pages_scraped: int
    total_organic_results: int
    organic_results: List[OrganicItem]
    people_also_ask: Optional[List[Dict[str, str]]] = None
    sponsored_ads: Optional[List[Dict[str, Any]]] = None

class SearchAPIResponse(BaseModel):
    status: str
    total_queries: int
    results: List[SearchResponseItem]

# ==============================================================================
# API Endpoints
# ==============================================================================
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Google SERP & Search Intelligence Extractor API",
        "version": "1.0.0"
    }

@app.post("/api/v1/search", response_model=SearchAPIResponse)
def execute_serp_search(payload: SearchRequest):
    if not payload.search_queries:
        raise HTTPException(status_code=400, detail="search_queries list cannot be empty.")

    extracted_results = []
    for query in payload.search_queries[:10]:  # Cap at 10 queries per request
        res = scrape_google_serp(
            query=query.strip(),
            page_depth=payload.page_depth or 1,
            country_code=payload.country_code or "us",
            language_code=payload.language_code or "en",
            include_paa=payload.include_paa if payload.include_paa is not None else True,
            include_paid_ads=payload.include_paid_ads if payload.include_paid_ads is not None else True
        )
        extracted_results.append(res)

    return SearchAPIResponse(
        status="success",
        total_queries=len(extracted_results),
        results=extracted_results
    )

@app.get("/api/v1/search")
def execute_serp_search_get(
    q: str = Query(..., description="Target search query"),
    page_depth: int = Query(default=1, ge=1, le=5),
    country_code: str = Query(default="us"),
    language_code: str = Query(default="en")
):
    res = scrape_google_serp(
        query=q.strip(),
        page_depth=page_depth,
        country_code=country_code,
        language_code=language_code
    )
    return {
        "status": "success",
        "result": res
    }
