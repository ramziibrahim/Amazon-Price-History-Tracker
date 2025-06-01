import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .models import PriceHistoryRequest, PriceHistoryResponse, ErrorResponse
from .scraper import fetch_history, extract_asin, ScraperError

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Amazon Price History API",
    description="API for fetching Amazon product price history",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/api/history",
    response_model=PriceHistoryResponse,
    responses={
        404: {"model": ErrorResponse},
        502: {"model": ErrorResponse}
    }
)
async def get_price_history(request: PriceHistoryRequest):
    try:
        # Extract ASIN from URL
        asin = extract_asin(str(request.url))
        
        # Fetch price history
        history = fetch_history(asin, os.getenv("DOWNLOAD_DIR", "/app/downloads"))
        
        if not history:
            raise HTTPException(
                status_code=404,
                detail="No price history found for this product"
            )
            
        return PriceHistoryResponse(asin=asin, history=history)
        
    except ScraperError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 