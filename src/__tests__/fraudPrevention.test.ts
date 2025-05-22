import {
  FraudPreventionEntity,
  RiskLevel,
} from "../entity/fraudPreventionEntity";
import { AppDataSource } from "../datasource/datasource";
import { Repository } from "typeorm";
import { FraudPreventionController } from "../controllers/fraudPreventionController";
import { Request, Response } from "express";

describe("Fraud Prevention Tests", () => {
  let fraudPreventionController: FraudPreventionController;
  let mockRepository: Partial<Repository<FraudPreventionEntity>>;
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;

  beforeEach(() => {
    mockRepository = {
      find: jest.fn(),
      findOne: jest.fn(),
      save: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    };

    // Mock the response object
    mockResponse = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn().mockReturnThis(),
    };

    // Mock AppDataSource.getRepository
    jest
      .spyOn(AppDataSource, "getRepository")
      .mockReturnValue(mockRepository as Repository<FraudPreventionEntity>);

    fraudPreventionController = new FraudPreventionController();
  });

  describe("Create Fraud Prevention", () => {
    it("should create a new fraud prevention record", async () => {
      const mockFraudPrevention = {
        transactionId: "123",
        userIp: "192.168.1.1",
        deviceId: "device123",
        userId: "user123",
        riskLevel: RiskLevel.LOW,
      };

      mockRequest = {
        body: mockFraudPrevention,
      };

      (mockRepository.save as jest.Mock).mockResolvedValue(mockFraudPrevention);

      await fraudPreventionController.create(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(mockRepository.save).toHaveBeenCalledWith(
        expect.objectContaining(mockFraudPrevention)
      );
      expect(mockResponse.status).toHaveBeenCalledWith(201);
      expect(mockResponse.json).toHaveBeenCalledWith(
        expect.objectContaining(mockFraudPrevention)
      );
    });
  });

  describe("Get Fraud Prevention", () => {
    it("should get fraud prevention by ID", async () => {
      const mockFraudPrevention = {
        id: "123",
        transactionId: "123",
        userIp: "192.168.1.1",
      };

      mockRequest = {
        params: { id: "123" },
      };

      (mockRepository.findOne as jest.Mock).mockResolvedValue(
        mockFraudPrevention
      );

      await fraudPreventionController.getById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(mockRepository.findOne).toHaveBeenCalledWith({
        where: { id: "123" },
      });
      expect(mockResponse.json).toHaveBeenCalledWith(mockFraudPrevention);
    });

    it("should return 404 when fraud prevention not found", async () => {
      mockRequest = {
        params: { id: "nonexistent" },
      };

      (mockRepository.findOne as jest.Mock).mockResolvedValue(null);

      await fraudPreventionController.getById(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(mockResponse.status).toHaveBeenCalledWith(404);
    });
  });

  describe("Block Transaction", () => {
    it("should block a transaction", async () => {
      const mockFraudPrevention = {
        id: "123",
        transactionId: "123",
        isBlocked: false,
      };

      mockRequest = {
        params: { id: "123" },
        body: { reason: "Suspicious activity" },
      };

      (mockRepository.findOne as jest.Mock).mockResolvedValue(
        mockFraudPrevention
      );
      (mockRepository.save as jest.Mock).mockResolvedValue({
        ...mockFraudPrevention,
        isBlocked: true,
        blockReason: "Suspicious activity",
      });

      await fraudPreventionController.blockTransaction(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(mockRepository.save).toHaveBeenCalledWith(
        expect.objectContaining({
          isBlocked: true,
          blockReason: "Suspicious activity",
        })
      );
      expect(mockResponse.json).toHaveBeenCalled();
    });
  });

  describe("Risk Level Assessment", () => {
    it("should update risk level based on attempt count", async () => {
      const mockFraudPrevention = {
        id: "123",
        transactionId: "123",
        attemptCount: 5,
        riskLevel: RiskLevel.LOW,
      };

      mockRequest = {
        body: mockFraudPrevention,
      };

      (mockRepository.save as jest.Mock).mockImplementation((entity) => {
        if (entity.attemptCount >= 5) {
          entity.riskLevel = RiskLevel.HIGH;
        }
        return Promise.resolve(entity);
      });

      await fraudPreventionController.create(
        mockRequest as Request,
        mockResponse as Response
      );

      expect(mockRepository.save).toHaveBeenCalledWith(
        expect.objectContaining({
          riskLevel: RiskLevel.HIGH,
        })
      );
    });
  });
});
