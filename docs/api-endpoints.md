# API Endpoints

All endpoints are prefixed with `/api/fraud-preventions`

## Create Fraud Prevention Record
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

## Get All Fraud Preventions
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

## Get by ID
- **GET** `/{fraud_id}`
- **Response** (200 OK): FraudPreventionResponse object
- **Response** (404 Not Found):
```json
{
    "detail": "Fraud prevention record not found"
}
```

## Get by Transaction ID
- **GET** `/transaction/{transaction_id}`
- **Response** (200 OK): FraudPreventionResponse object
- **Response** (404 Not Found):
```json
{
    "detail": "Fraud prevention record not found"
}
```

## Get by User ID
- **GET** `/user/{user_id}`
- **Response** (200 OK): Array of FraudPreventionResponse objects

## Update Fraud Prevention
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

## Block Transaction
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

## Risk Levels
Available risk levels for transactions:
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL` 