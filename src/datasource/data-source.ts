import { DataSource } from "typeorm";
import { FraudPreventionEntity } from "../entity/fraudPreventionEntity";

export const AppDataSource = new DataSource({
    type: "mysql",
    host: process.env.DB_HOST || "localhost",
    port: parseInt(process.env.DB_PORT || "3306"),
    username: process.env.DB_USER || "root",
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME || "fraud_prevention_db",
    synchronize: false,
    logging: process.env.NODE_ENV !== "production",
    entities: [FraudPreventionEntity],
    migrations: ["dist/migrations/*.js"],
    subscribers: [],
}); 