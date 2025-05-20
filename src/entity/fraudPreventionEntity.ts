import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn } from "typeorm";

export enum RiskLevel {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  CRITICAL = "critical"
}

@Entity("fraud_prevention")
export class FraudPreventionEntity {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column({ type: "varchar", length: 255, nullable: false })
  transactionId: string;

  @Column({ type: "varchar", length: 100, nullable: false })
  userIp: string;

  @Column({ type: "varchar", length: 255, nullable: true })
  deviceId: string;

  @Column({ type: "varchar", length: 255, nullable: false })
  userId: string;

  @Column({ 
    type: "enum", 
    enum: RiskLevel,
    default: RiskLevel.LOW 
  })
  riskLevel: RiskLevel;

  @Column({ type: "json", nullable: true })
  additionalData: any;

  @Column({ type: "boolean", default: false })
  isBlocked: boolean;

  @Column({ type: "text", nullable: true })
  blockReason: string;

  @Column({ type: "int", default: 0 })
  attemptCount: number;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}