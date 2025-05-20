import { Repository } from "typeorm";
import { AppDataSource } from "../datasource/datasource";
import { FraudPreventionEntity, RiskLevel } from "../entity/fraudPreventionEntity";

export class FraudPreventionService {
  private fraudPreventionRepository: Repository<FraudPreventionEntity>;

  constructor() {
    this.fraudPreventionRepository = AppDataSource.getRepository(FraudPreventionEntity);
  }

  async findAll(page: number = 1, limit: number = 10): Promise<{ data: FraudPreventionEntity[], total: number, page: number, pages: number }> {
    const [data, total] = await this.fraudPreventionRepository.findAndCount({
      take: limit,
      skip: (page - 1) * limit,
      order: { createdAt: "DESC" }
    });

    return {
      data,
      total,
      page,
      pages: Math.ceil(total / limit)
    };
  }

  async findById(id: string): Promise<FraudPreventionEntity | null> {
    return this.fraudPreventionRepository.findOne({
      where: { id }
    });
  }

  async findByTransactionId(transactionId: string): Promise<FraudPreventionEntity | null> {
    return this.fraudPreventionRepository.findOne({
      where: { transactionId }
    });
  }

  async findByUserId(userId: string): Promise<FraudPreventionEntity[]> {
    return this.fraudPreventionRepository.find({
      where: { userId },
      order: { createdAt: "DESC" }
    });
  }

  async create(fraudPreventionData: Partial<FraudPreventionEntity>): Promise<FraudPreventionEntity> {
    const fraudPrevention = this.fraudPreventionRepository.create(fraudPreventionData);
    return await this.fraudPreventionRepository.save(fraudPrevention);
  }

  async update(id: string, fraudPreventionData: Partial<FraudPreventionEntity>): Promise<FraudPreventionEntity | null> {
    const fraudPrevention = await this.findById(id);
    
    if (!fraudPrevention) {
      return null;
    }

    Object.assign(fraudPrevention, fraudPreventionData);
    return await this.fraudPreventionRepository.save(fraudPrevention);
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.fraudPreventionRepository.delete(id);
    return result.affected !== 0;
  }

  async assessRisk(transactionData: any): Promise<RiskLevel> {
    // Implementar lógica de evaluación de riesgo
    // Este es un ejemplo simplificado
    let riskScore = 0;
    
    // Verificar intentos anteriores
    const previousAttempts = await this.fraudPreventionRepository.count({
      where: {
        userId: transactionData.userId,
        createdAt: new Date(new Date().setDate(new Date().getDate() - 1)) // Últimas 24 horas
      }
    });
    
    if (previousAttempts > 10) riskScore += 30;
    else if (previousAttempts > 5) riskScore += 15;
    
    // Verificar IP
    const multipleIpUsers = await this.fraudPreventionRepository.count({
      where: {
        userIp: transactionData.userIp,
        userId: transactionData.userId
      }
    });
    
    if (multipleIpUsers > 3) riskScore += 25;
    
    // Asignar nivel de riesgo
    if (riskScore >= 50) return RiskLevel.CRITICAL;
    if (riskScore >= 30) return RiskLevel.HIGH;
    if (riskScore >= 15) return RiskLevel.MEDIUM;
    return RiskLevel.LOW;
  }

  async blockTransaction(id: string, reason: string): Promise<FraudPreventionEntity | null> {
    const fraudPrevention = await this.findById(id);
    
    if (!fraudPrevention) {
      return null;
    }
    
    fraudPrevention.isBlocked = true;
    fraudPrevention.blockReason = reason;
    
    return await this.fraudPreventionRepository.save(fraudPrevention);
  }
}