#!/bin/sh

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo "Running database migrations..."
npm run migration:run

# Start the application
echo "Starting the application..."
node dist/index.js 