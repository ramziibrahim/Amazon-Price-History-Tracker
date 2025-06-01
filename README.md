# Amazon Price History Tracker

A full-stack application that tracks and visualizes Amazon product price history using data from camelcamelcamel.com.


curl -X POST http://localhost:8000/api/history \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.com/dp/B07TEST123"}'


## Project Structure

```
.
├── backend/
│   ├── main.py           # FastAPI application
│   ├── scraper.py        # Price history scraper
│   ├── models.py         # Pydantic models
│   ├── tests/            # Test files
│   └── Dockerfile        # Backend container configuration
├── web/
│   ├── src/
│   │   ├── app/         # Next.js pages
│   │   └── components/  # React components
│   └── Dockerfile       # Frontend container configuration
└── docker-compose.yml   # Multi-container configuration
```
