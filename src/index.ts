import express from 'express';
import cors from 'cors';
import { fraudPreventionRouter } from './routes/fraudPreventionRouter';
import { AppDataSource } from './datasource/data-source';

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK' });
});

// Initialize database connection
AppDataSource.initialize()
  .then(() => {
    console.log("Database connection initialized");
  })
  .catch((error) => {
    console.error("Error initializing database connection:", error);
  });

app.use('/api/fraud-preventions', fraudPreventionRouter);

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});