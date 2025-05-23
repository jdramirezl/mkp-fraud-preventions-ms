#!/bin/sh

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo "Running database migrations..."
NODE_ENV=production npx typeorm-ts-node-commonjs migration:run -d dist/datasource/data-source.js

if [ $? -ne 0 ]; then
    echo "Migration failed! Check the logs above for details."
    exit 1
fi

# Start the application
echo "Starting the application..."
echo "Using PORT: $PORT"
NODE_ENV=production node dist/index.js 