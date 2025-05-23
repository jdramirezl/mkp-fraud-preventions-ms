import { DataSource, DataSourceOptions } from "typeorm";
import { FraudPreventionEntity } from "../entity/fraudPreventionEntity";

const getConnectionConfig = (): DataSourceOptions => {
  const baseConfig = {
    type: "mysql" as const,
    synchronize: false,
    logging: process.env.NODE_ENV !== "production",
    entities: [FraudPreventionEntity],
    migrations: ["dist/migrations/*.js"],
    subscribers: [],
  };

  if (process.env.NODE_ENV === 'production') {
    // In Cloud Run, use Unix socket
    return {
      ...baseConfig,
      socketPath: `/cloudsql/${process.env.INSTANCE_CONNECTION_NAME}`,
      username: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME,
    };
  }

  // Local development
  return {
    ...baseConfig,
    host: process.env.DB_HOST || "localhost",
    port: parseInt(process.env.DB_PORT || "3306"),
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
  };
};

export const AppDataSource = new DataSource(getConnectionConfig()); 