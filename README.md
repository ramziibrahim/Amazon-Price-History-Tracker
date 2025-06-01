# Amazon Price History Tracker

A full-stack application that tracks and visualizes Amazon product price history using data from camelcamelcamel.com.

## Features

- Fetch price history for any Amazon product using its URL or ASIN
- Interactive price history chart with date and price information
- Real-time price data from camelcamelcamel.com
- Modern, responsive UI built with Next.js and Tailwind CSS
- FastAPI backend with browser automation for data scraping

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd amazon-price-tracker
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API Documentation: http://localhost:8000/docs

## Usage

1. Open the frontend application in your browser (http://localhost:3000)
2. Enter an Amazon product URL (e.g., https://www.amazon.com/dp/B07TEST123)
3. Click "Fetch Price History" to view the price history chart

## API Example

You can also use the API directly:

```bash
curl -X POST http://localhost:8000/api/history \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.com/dp/B07TEST123"}'
```

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

## Error Handling

The application handles various error cases:
- Invalid Amazon URLs
- Missing price history data
- Network timeouts
- Service unavailability

Error messages are displayed in the UI and returned as appropriate HTTP status codes in the API.

## Development

To run tests:
```bash
cd backend
pytest
```

## License

MIT 