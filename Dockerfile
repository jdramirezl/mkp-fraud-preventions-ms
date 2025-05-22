FROM node:21

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# TypeScript compilation
RUN npm run build

EXPOSE 3000

# Use nodemon for development
CMD ["npm", "start"]