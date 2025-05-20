import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import 'dotenv/config';
import { AppDataSource } from "./datasource/datasource";
import { fraudPreventionRouter } from './routes/fraudPreventionRouter';


AppDataSource.connect()
  .then(() => {
    console.log('Database connection established');
  })
  .catch((error: Error) => {
    console.error('Database connection failed', error);
  });

const app = express();  

// Middlewares
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());
app.use(morgan('dev'));

// Routes
app.use('/api/fraud-preventions', fraudPreventionRouter);

// Health check
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK' });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});