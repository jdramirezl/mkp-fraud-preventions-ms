import { DataSource } from "typeorm";
import { FraudPreventionEntity } from "../entity/fraudPreventionEntity";

export const AppDataSource = new DataSource({
    type: "mysql",
    host: process.env.DB_HOST || "localhost",
    port: parseInt(process.env.DB_PORT || "3306"),
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    synchronize: false,
    logging: true,
    entities: [FraudPreventionEntity],
    migrations: ["src/migrations/*.ts"],
    subscribers: [],
}); 