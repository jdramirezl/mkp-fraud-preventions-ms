import { FraudPreventionService } from '../services/fraudPreventionService';
import { AppDataSource } from '../datasource/datasource';
import { RiskLevel } from '../entity/fraudPreventionEntity';

describe('FraudPreventionService', () => {
  let service: FraudPreventionService;

  beforeEach(() => {
    service = new FraudPreventionService();
  });

  describe('create', () => {
    it('should create a fraud prevention record', async () => {
      const data = {
        transactionId: '123',
        userIp: '192.168.1.1',
        deviceId: 'device123',
        userId: 'user123',
        riskLevel: RiskLevel.LOW,
      };

      const result = await service.create(data);

      expect(result).toEqual(expect.objectContaining(data));
      expect(result.id).toBeDefined();
    });
  });

  describe('assessRisk', () => {
    it('should assess risk as HIGH for suspicious IP', async () => {
      const data = {
        transactionId: '123',
        userIp: '192.168.1.1',
        userId: 'user123',
      };

      const result = await service.assessRisk(data);
      expect(result).toBe(RiskLevel.HIGH);
    });

    it('should assess risk as LOW for normal transaction', async () => {
      const data = {
        transactionId: '123',
        userIp: '8.8.8.8', // Google DNS IP
        userId: 'user123',
      };

      const result = await service.assessRisk(data);
      expect(result).toBe(RiskLevel.LOW);
    });
  });

  describe('findById', () => {
    it('should find a fraud prevention record by ID', async () => {
      const data = {
        transactionId: '123',
        userIp: '192.168.1.1',
        riskLevel: RiskLevel.LOW,
      };
      
      const created = await service.create(data);
      const found = await service.findById(created.id);
      
      expect(found).toEqual(created);
    });

    it('should return null for non-existent ID', async () => {
      const result = await service.findById('nonexistent');
      expect(result).toBeNull();
    });
  });

  describe('findByTransactionId', () => {
    it('should find records by transaction ID', async () => {
      const data = {
        transactionId: 'tx123',
        userIp: '192.168.1.1',
        riskLevel: RiskLevel.LOW,
      };
      
      await service.create(data);
      const results = await service.findByTransactionId('tx123');
      
      expect(results).toHaveLength(1);
      expect(results[0]).toEqual(expect.objectContaining(data));
    });
  });

  describe('findByUserId', () => {
    it('should find records by user ID', async () => {
      const data = {
        transactionId: '123',
        userIp: '192.168.1.1',
        userId: 'user123',
        riskLevel: RiskLevel.LOW,
      };
      
      await service.create(data);
      const results = await service.findByUserId('user123');
      
      expect(results).toHaveLength(1);
      expect(results[0]).toEqual(expect.objectContaining(data));
    });
  });

  describe('blockTransaction', () => {
    it('should block a transaction', async () => {
      const data = {
        transactionId: '123',
        userIp: '192.168.1.1',
        riskLevel: RiskLevel.LOW,
        isBlocked: false,
      };
      
      const created = await service.create(data);
      const blocked = await service.blockTransaction(created.id, 'Suspicious activity');
      
      expect(blocked).toBeDefined();
      expect(blocked?.isBlocked).toBe(true);
      expect(blocked?.blockReason).toBe('Suspicious activity');
    });

    it('should return null for non-existent transaction', async () => {
      const result = await service.blockTransaction('nonexistent', 'test');
      expect(result).toBeNull();
    });
  });
}); 