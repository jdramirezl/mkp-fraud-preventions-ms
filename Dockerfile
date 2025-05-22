# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# TypeScript compilation
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy package files and install production dependencies
COPY package*.json ./
RUN npm install --production

# Copy compiled files and necessary source files for TypeORM
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/src/migrations ./src/migrations
COPY --from=builder /app/src/entity ./src/entity
COPY --from=builder /app/src/datasource ./src/datasource
COPY --from=builder /app/tsconfig.json ./

# Add TypeScript dependencies for migrations
RUN npm install -D typescript ts-node @types/node

# Add a startup script
COPY start.sh .
RUN chmod +x start.sh

# Set environment variables
ENV PORT=8080
ENV NODE_ENV=production

EXPOSE 8080

CMD ["./start.sh"]