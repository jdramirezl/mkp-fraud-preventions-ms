# Development Guide

## Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd fraud-prevention-ms
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Start the development environment:
```bash
docker-compose up
```

The API will be available at `http://localhost:8000`

## Testing

Run tests with coverage:
```bash
pytest --cov=src --cov-report=xml
```

## Development Workflow

1. Create a feature branch
2. Make changes and test locally
3. Create a PR to main/master
4. GitHub Actions runs tests
5. After approval and merge:
   - New image is built and pushed
   - Cloud Run service updates automatically

## Environment Variables

### Local Development
```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=fraud_prevention
DB_HOST=localhost
DB_PORT=5432
```

### Production
Environment variables are managed through Terraform and Cloud Run configuration.

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD workflow
├── src/
│   ├── database/          # Database configuration
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # API endpoints
│   ├── schemas/           # Pydantic models
│   ├── services/          # Business logic
│   └── main.py           # Application entry
├── terraform/
│   ├── main.tf           # Main Terraform configuration
│   ├── variables.tf      # Variable definitions
│   └── outputs.tf        # Output definitions
├── tests/                # Test suite
├── Dockerfile           # Production container
├── docker-compose.yml   # Local development
├── requirements.txt     # Python dependencies
└── README.md
``` 