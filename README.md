# Fraud Prevention Microservice

A microservice for fraud prevention and risk assessment, built with FastAPI and SQLAlchemy.

## 🚀 Features

- Real-time fraud risk assessment
- Transaction blocking
- User risk profiling
- REST API with OpenAPI documentation
- PostgreSQL database with Cloud SQL
- Automated CI/CD with GitHub Actions
- Infrastructure as Code with Terraform
- Containerized deployment on Cloud Run

## 🛠️ Tech Stack

- Python 3.12
- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Terraform (Infrastructure as Code)
- Google Cloud Platform
  - Cloud Run (Serverless deployment)
  - Cloud SQL (Managed PostgreSQL)
  - Artifact Registry (Container registry)

## 📚 Documentation

- [API Endpoints](docs/api-endpoints.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)
- [Integration Guide](docs/integration.md)

## 🏗️ Local Development

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

## 📚 API Documentation

Once the service is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

Run tests with coverage:
```bash
pytest --cov=src --cov-report=xml
```

## 🚢 Production Deployment

### Prerequisites

1. **Google Cloud Platform Setup**
   - Create a new project or use an existing one
   - Enable required APIs:
     - Cloud Run API
     - Cloud SQL Admin API
     - Artifact Registry API
   - Create a service account with necessary permissions
   - Download the service account key JSON

2. **GitHub Repository Setup**
   Add the following secrets:
   - `GCP_SA_KEY`: The service account key JSON
   - `PROJECT_ID`: Your GCP project ID

### Deployment Process

The deployment is fully automated through GitHub Actions and Terraform:

1. **CI/CD Pipeline** (.github/workflows/deploy.yml)
   - Runs on:
     - Pull requests (tests only)
     - Pushes to main/master (full deployment)
     - Manual triggers
   - Steps:
     - Runs tests and coverage
     - Builds Docker image
     - Pushes to Artifact Registry
     - Updates Cloud Run service

2. **Infrastructure** (terraform/)
   - Managed resources:
     - Cloud SQL PostgreSQL instance
     - Cloud Run service
     - IAM permissions
     - Network configuration

### Manual Deployment

If needed, you can deploy manually:

1. Build and push the Docker image:
```bash
docker build -t us-central1-docker.pkg.dev/PROJECT_ID/fraud-prevention/fraud-prevention-api:latest .
docker push us-central1-docker.pkg.dev/PROJECT_ID/fraud-prevention/fraud-prevention-api:latest
```

2. Apply Terraform configuration:
```bash
cd terraform
terraform init
terraform apply
```

## 🔌 Integration Guide

To integrate with this microservice:

1. **Base URL**: 
```
https://fraud-prevention-api-fuylmr6llq-uc.a.run.app
```

2. **Environment Variables**:
```env
FRAUD_PREVENTION_API_URL=https://fraud-prevention-api-fuylmr6llq-uc.a.run.app
```

3. **API Documentation**:
   - Swagger UI: `${FRAUD_PREVENTION_API_URL}/docs`
   - ReDoc: `${FRAUD_PREVENTION_API_URL}/redoc`

## 📦 Project Structure

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

## 🔒 Security Considerations

1. **Database Security**
   - Cloud SQL instance with private IP
   - SSL/TLS encryption for connections
   - Managed backups and updates

2. **API Security**
   - HTTPS only
   - Cloud Run's built-in security
   - Input validation with Pydantic

3. **CI/CD Security**
   - Secrets managed via GitHub Actions
   - Least privilege service accounts
   - Container vulnerability scanning

## 🔄 Development Workflow

1. Create a feature branch
2. Make changes and test locally
3. Create a PR to main/master
4. GitHub Actions runs tests
5. After approval and merge:
   - New image is built and pushed
   - Cloud Run service updates automatically

## 📋 Environment Variables

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For any questions or suggestions, please open an issue in the repository.

## 📡 API Endpoints

All endpoints are prefixed with `/api/fraud-preventions`

### Create Fraud Prevention Record
- **POST** `/`
- **Request Body**:
```json
{
    "transactionId": "tx-123456",
    "userIp": "192.168.1.1",
    "deviceId": "device-xyz-123",  // optional
    "userId": "user-123",
    "additionalData": {            // optional
        "amount": 1000,
        "currency": "USD",
        "paymentMethod": "credit_card"
    }
}
```
- **Response** (200 OK):
```json
{
    "id": "uuid-123",
    "transactionId": "tx-123456",
    "userIp": "192.168.1.1",
    "deviceId": "device-xyz-123",
    "userId": "user-123",
    "additionalData": {
        "amount": 1000,
        "currency": "USD",
        "paymentMethod": "credit_card"
    },
    "riskLevel": "LOW",
    "isBlocked": false,
    "blockReason": null,
    "attemptCount": 1,
    "createdAt": "2025-05-24T17:12:46Z",
    "updatedAt": "2025-05-24T17:12:46Z"
}
```

### Get All Fraud Preventions
- **GET** `/?page=1&limit=10`
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 10, max: 100)
- **Response** (200 OK):
```json
{
    "data": [
        {
            // FraudPreventionResponse object
        }
    ],
    "total": 100,
    "page": 1,
    "pages": 10
}
```

### Get by ID
- **GET** `/{fraud_id}`
- **Response** (200 OK): FraudPreventionResponse object
- **Response** (404 Not Found):
```json
{
    "detail": "Fraud prevention record not found"
}
```

### Get by Transaction ID
- **GET** `/transaction/{transaction_id}`
- **Response** (200 OK): FraudPreventionResponse object
- **Response** (404 Not Found):
```json
{
    "detail": "Fraud prevention record not found"
}
```

### Get by User ID
- **GET** `/user/{user_id}`
- **Response** (200 OK): Array of FraudPreventionResponse objects

### Update Fraud Prevention
- **PATCH** `/{fraud_id}`
- **Request Body**:
```json
{
    "riskLevel": "HIGH",           // optional
    "isBlocked": true,            // optional
    "blockReason": "Suspicious activity",  // optional
    "attemptCount": 3             // optional
}
```
- **Response** (200 OK): FraudPreventionResponse object
- **Response** (404 Not Found):
```json
{
    "detail": "Fraud prevention record not found"
}
```

### Block Transaction
- **POST** `/{fraud_id}/block`
- **Request Body**:
```json
{
    "reason": "Multiple failed attempts from different locations"
}
```
- **Response** (200 OK): FraudPreventionResponse object
- **Response** (404 Not Found):
```json
{
    "detail": "Fraud prevention record not found"
}
```

### Risk Levels
Available risk levels for transactions:
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

---

Made with ❤️ by the Fraud Prevention Team
