import { DataSource } from "typeorm";
import dotenv from "dotenv";
import { FraudPreventionEntity } from "../entity/fraudPreventionEntity";

// Load environment variables
dotenv.config();

const isProd = process.env.NODE_ENV === "production";

export const AppDataSource = new DataSource({
  type: "mysql",
  host: process.env.DB_HOST || "db-fraud-preventions",
  port: parseInt(process.env.DB_PORT || "3306"),
  username: process.env.DB_USER || "root",
  password: process.env.DB_PASSWORD || "root",
  database: process.env.DB_NAME || "fraud_prevention_db",
  synchronize: false, // Never true in production
  logging: !isProd,
  entities: [FraudPreventionEntity],
  migrations: ["dist/migrations/*.js"],
  migrationsRun: true, // Automatically run migrations on startup
});
