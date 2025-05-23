# Fraud Prevention Microservice

A robust TypeScript microservice for fraud detection and prevention in digital transactions.

## 📋 Features

- **Real-time Risk Assessment** - Automatic transaction analysis to determine risk levels
- **User and Device Tracking** - Monitoring of suspicious behavior patterns
- **Complete RESTful API** - Endpoints for all CRUD operations
- **Transaction Blocking** - Ability to block suspicious transactions with reason logging
- **MySQL Persistence** - Secure and efficient data storage
- **Docker Containerization** - Easy deployment in any environment

## 🛠️ Architecture

The microservice follows a layered architecture:

```
fraud-preventions-ms/
├── src/
│   ├── controllers/     # HTTP request handling
│   ├── datasource/      # Database connection configuration
│   ├── entity/          # Entity and model definitions
│   ├── routes/          # API route definitions
│   ├── services/        # Business logic
│   └── index.ts         # Application entry point
```

## 🚀 Deployment Setup

### Prerequisites

1. **Google Cloud Platform Account**
   - Create a new project or use an existing one
   - Enable the required APIs (will be handled by Terraform)
   - Create a service account with the following roles:
     - Cloud Run Admin
     - Cloud SQL Admin
     - Storage Admin
     - Service Account User
     - Artifact Registry Administrator

2. **GitHub Repository Setup**
   Add the following secrets to your GitHub repository:
   - `GCP_PROJECT_ID`: Your GCP project ID
   - `GCP_SA_KEY`: The service account key JSON
   - `GCP_TF_STATE_BUCKET`: The GCS bucket name for Terraform state
   - `DB_PASSWORD`: The password for the database user

### Infrastructure

The infrastructure is managed using Terraform and includes:
- Cloud Run service for the application
- Cloud SQL (MySQL) for the database
- Artifact Registry for Docker images
- Required networking and IAM configurations

### CI/CD Pipeline

The GitHub Actions workflow (`ci-cd.yml`) handles:
1. Running tests
2. Building the Docker image
3. Pushing to Artifact Registry
4. Applying Terraform changes
5. Deploying to Cloud Run

## 💻 Local Development

1. **Clone the repository**
```bash
   git clone git@github.com:jdramirezl/mkp-fraud-preventions-ms.git
   cd mkp-fraud-preventions-ms
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
   Create a `.env` file:
   ```env
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
   DB_PASSWORD=your_password
   DB_DATABASE=fraud_prevention_db
NODE_ENV=development
```

4. **Run locally**
```bash
npm run dev
```

5. **Run with Docker**
```bash
   docker-compose up
```

## 📡 API Endpoints

### Fraud Prevention

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/fraud-preventions` | Get all fraud preventions (paginated) |
| GET | `/api/fraud-preventions/:id` | Get fraud prevention by ID |
| GET | `/api/fraud-preventions/transaction/:transactionId` | Get prevention by transaction ID |
| GET | `/api/fraud-preventions/user/:userId` | Get all preventions for a user |
| POST | `/api/fraud-preventions` | Create new fraud prevention record |
| PUT | `/api/fraud-preventions/:id` | Update existing record |
| DELETE | `/api/fraud-preventions/:id` | Delete record |
| POST | `/api/fraud-preventions/:id/block` | Block a transaction with specific reason |

### Service Health

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Check service health status |

## 📥 Usage Examples

### Create a New Fraud Check

```bash
curl -X POST http://localhost:3000/api/fraud-preventions \
  -H "Content-Type: application/json" \
  -d '{
    "transactionId": "tx-123456789",
    "userIp": "192.168.1.1",
    "deviceId": "device-xyz-123",
    "userId": "user-abc-456",
    "additionalData": {
      "amount": 1000,
      "currency": "USD",
      "paymentMethod": "credit_card"
    }
  }'
```

### Block a Suspicious Transaction

```bash
curl -X POST http://localhost:3000/api/fraud-preventions/uuid-of-record/block \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Multiple failed attempts from different locations"
  }'
```

## 📊 Data Model

The main `FraudPrevention` entity contains:

- `id`: Unique identifier (UUID)
- `transactionId`: Related transaction ID
- `userIp`: User's IP address
- `deviceId`: Device identifier
- `userId`: User identifier
- `riskLevel`: Risk level (LOW, MEDIUM, HIGH, CRITICAL)
- `additionalData`: Additional transaction data (JSON)
- `isBlocked`: Transaction block indicator
- `blockReason`: Block reason
- `attemptCount`: Attempt counter
- `createdAt`: Creation timestamp
- `updatedAt`: Last update timestamp

## 🧪 Development Cycle

1. **Run Tests**
```bash
npm run test
```

2. **Build TypeScript**
```bash
npm run build
```

3. **Lint Code**
```bash
npm run lint
```

4. **Run Production Server**
```bash
npm start
```

## 🚢 Production Deployment

1. Configure production environment variables
2. Build Docker image:
```bash
docker build -t fraud-preventions-ms:latest .
```

3. Run with appropriate configuration:
```bash
   docker run -p 3000:8080 --env-file .env.production fraud-preventions-ms:latest
```

## 📚 API Documentation

The API documentation is available through Swagger UI when running in development mode.

## 🔒 Security Considerations

1. **Database Access**
   - Cloud SQL instance is protected by authorized networks
   - Credentials are managed through GitHub Secrets
   - SSL/TLS encryption for database connections

2. **API Security**
   - Cloud Run service can be configured with authentication
   - Environment variables are securely managed
   - Service account with minimal required permissions

## 📊 Monitoring and Logging

- Cloud Run provides built-in monitoring and logging
- Cloud SQL monitoring is available through Cloud Monitoring
- Custom metrics can be added using OpenTelemetry

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For any questions or suggestions, please open an issue in the repository.

---

Made with ❤️ by the Fraud Prevention Team
