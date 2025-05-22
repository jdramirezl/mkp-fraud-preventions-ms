import { MigrationInterface, QueryRunner, Table } from "typeorm";
import { RiskLevel } from "../entity/FraudPreventionEntity";

export class CreateFraudPreventionTable1710965644123 implements MigrationInterface {
    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(
            new Table({
                name: "fraud_prevention",
                columns: [
                    {
                        name: "id",
                        type: "varchar",
                        isPrimary: true,
                        generationStrategy: "uuid"
                    },
                    {
                        name: "transactionId",
                        type: "varchar",
                        length: "255",
                        isNullable: false
                    },
                    {
                        name: "userIp",
                        type: "varchar",
                        length: "100",
                        isNullable: false
                    },
                    {
                        name: "deviceId",
                        type: "varchar",
                        length: "255",
                        isNullable: true
                    },
                    {
                        name: "userId",
                        type: "varchar",
                        length: "255",
                        isNullable: false
                    },
                    {
                        name: "riskLevel",
                        type: "enum",
                        enum: Object.values(RiskLevel),
                        default: `'${RiskLevel.LOW}'`
                    },
                    {
                        name: "additionalData",
                        type: "json",
                        isNullable: true
                    },
                    {
                        name: "isBlocked",
                        type: "boolean",
                        default: false
                    },
                    {
                        name: "blockReason",
                        type: "text",
                        isNullable: true
                    },
                    {
                        name: "attemptCount",
                        type: "int",
                        default: 0
                    },
                    {
                        name: "createdAt",
                        type: "timestamp",
                        default: "CURRENT_TIMESTAMP"
                    },
                    {
                        name: "updatedAt",
                        type: "timestamp",
                        default: "CURRENT_TIMESTAMP",
                        onUpdate: "CURRENT_TIMESTAMP"
                    }
                ]
            }),
            true
        );
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropTable("fraud_prevention");
    }
} 