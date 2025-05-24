# Integration Guide

## Base URL

```
https://fraud-prevention-api-fuylmr6llq-uc.a.run.app
```

## Environment Variables

Add these variables to your service's configuration:

```env
FRAUD_PREVENTION_API_URL=https://fraud-prevention-api-fuylmr6llq-uc.a.run.app
```

## API Documentation

- Swagger UI: `${FRAUD_PREVENTION_API_URL}/docs`
- ReDoc: `${FRAUD_PREVENTION_API_URL}/redoc`

## Example Integration

### Python with requests

```python
import requests

FRAUD_API_URL = "https://fraud-prevention-api-fuylmr6llq-uc.a.run.app"

def check_transaction(transaction_data):
    response = requests.post(
        f"{FRAUD_API_URL}/api/fraud-preventions",
        json={
            "transactionId": transaction_data["id"],
            "userIp": transaction_data["ip"],
            "userId": transaction_data["user_id"],
            "additionalData": {
                "amount": transaction_data["amount"],
                "currency": transaction_data["currency"]
            }
        }
    )
    return response.json()

def get_user_fraud_history(user_id):
    response = requests.get(f"{FRAUD_API_URL}/api/fraud-preventions/user/{user_id}")
    return response.json()
```

### JavaScript/TypeScript with axios

```typescript
import axios from 'axios';

const FRAUD_API_URL = "https://fraud-prevention-api-fuylmr6llq-uc.a.run.app";

async function checkTransaction(transactionData) {
    const response = await axios.post(`${FRAUD_API_URL}/api/fraud-preventions`, {
        transactionId: transactionData.id,
        userIp: transactionData.ip,
        userId: transactionData.userId,
        additionalData: {
            amount: transactionData.amount,
            currency: transactionData.currency
        }
    });
    return response.data;
}

async function getUserFraudHistory(userId) {
    const response = await axios.get(`${FRAUD_API_URL}/api/fraud-preventions/user/${userId}`);
    return response.data;
}
```

## Error Handling

Your integration should handle these HTTP status codes:

- `404`: Resource not found
- `400`: Bad request (invalid input)
- `500`: Internal server error

Example error handling:

```python
def safe_check_transaction(transaction_data):
    try:
        return check_transaction(transaction_data)
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            if e.response.status_code == 404:
                # Handle not found
                pass
            elif e.response.status_code == 400:
                # Handle invalid input
                pass
        # Handle other errors
        raise
```

## Best Practices

1. **Implement Retry Logic**
   - Use exponential backoff for retries
   - Set appropriate timeouts

2. **Cache Results**
   - Cache user fraud history
   - Implement cache invalidation

3. **Monitor Integration**
   - Log all API calls
   - Track response times
   - Monitor error rates 