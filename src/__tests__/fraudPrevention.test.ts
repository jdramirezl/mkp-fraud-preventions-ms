import {
  FraudPreventionEntity,
  RiskLevel,
} from "../entity/fraudPreventionEntity";
import { AppDataSource } from "../datasource/data-source";
import { Repository } from "typeorm";
import { FraudPreventionController } from "../controllers/fraudPreventionController";
import { Request, Response } from "express";
import { FraudPreventionService } from '../services/fraudPreventionService';

// Create a mock service class
class MockFraudPreventionService {
  create = jest.fn();
  findById = jest.fn();
  findAll = jest.fn();
  update = jest.fn();
  delete = jest.fn();
  blockTransaction = jest.fn();
  assessRisk = jest.fn();
  findByTransactionId = jest.fn();
  findByUserId = jest.fn();
}

describe("Fraud Prevention Tests", () => {
  let fraudPreventionController: FraudPreventionController;
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let mockService: MockFraudPreventionService;

  beforeEach(() => {
    // Mock the response object
    mockResponse = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn().mockReturnThis(),
    };

    // Create a new instance of mock service
    mockService = new MockFraudPreventionService();
    
    // Create controller with mocked service
    fraudPreventionController = new FraudPreventionController(mockService as unknown as FraudPreventionService);
  });

  afterEach(() => {
    jest.clearAllMocks();
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

      mockService.create.mockResolvedValue(mockFraudPrevention);
      mockService.assessRisk.mockResolvedValue(RiskLevel.LOW);

      await fraudPreventionController.create(mockRequest as Request, mockResponse as Response);

      expect(mockService.create).toHaveBeenCalledWith(expect.objectContaining(mockFraudPrevention));
      expect(mockResponse.status).toHaveBeenCalledWith(201);
      expect(mockResponse.json).toHaveBeenCalledWith(mockFraudPrevention);
    });

    it("should handle errors when creating fraud prevention", async () => {
      const mockError = new Error("Database error");
      mockRequest = {
        body: {},
      };

      mockService.create.mockRejectedValue(mockError);

      await fraudPreventionController.create(mockRequest as Request, mockResponse as Response);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.json).toHaveBeenCalledWith({
        message: "Error al crear la prevención de fraude",
      });
    });

    it("should assess risk when riskLevel is not provided", async () => {
      const mockData = {
        transactionId: "123",
        userIp: "192.168.1.1",
        userId: "user123",
      };

      const mockFraudPrevention = {
        ...mockData,
        riskLevel: RiskLevel.HIGH,
      };

      mockRequest = {
        body: mockData,
      };

      mockService.assessRisk.mockResolvedValue(RiskLevel.HIGH);
      mockService.create.mockResolvedValue(mockFraudPrevention);

      await fraudPreventionController.create(mockRequest as Request, mockResponse as Response);

      expect(mockService.assessRisk).toHaveBeenCalledWith(mockData);
      expect(mockService.create).toHaveBeenCalledWith(expect.objectContaining({
        ...mockData,
        riskLevel: RiskLevel.HIGH,
      }));
      expect(mockResponse.status).toHaveBeenCalledWith(201);
      expect(mockResponse.json).toHaveBeenCalledWith(mockFraudPrevention);
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

      mockService.findById.mockResolvedValue(mockFraudPrevention);

      await fraudPreventionController.getById(mockRequest as Request, mockResponse as Response);

      expect(mockService.findById).toHaveBeenCalledWith("123");
      expect(mockResponse.json).toHaveBeenCalledWith(mockFraudPrevention);
    });

    it("should return 404 when fraud prevention not found", async () => {
      mockRequest = {
        params: { id: "nonexistent" },
      };

      mockService.findById.mockResolvedValue(null);

      await fraudPreventionController.getById(mockRequest as Request, mockResponse as Response);

      expect(mockResponse.status).toHaveBeenCalledWith(404);
      expect(mockResponse.json).toHaveBeenCalledWith({
        message: "Prevención de fraude no encontrada",
      });
    });
  });

  describe("Block Transaction", () => {
    it("should block a transaction", async () => {
      const mockFraudPrevention = {
        id: "123",
        transactionId: "123",
        isBlocked: false,
      };

      const updatedMockFraudPrevention = {
        ...mockFraudPrevention,
        isBlocked: true,
        blockReason: "Suspicious activity",
      };

      mockRequest = {
        params: { id: "123" },
        body: { reason: "Suspicious activity" },
      };

      mockService.blockTransaction.mockResolvedValue(updatedMockFraudPrevention);

      await fraudPreventionController.blockTransaction(mockRequest as Request, mockResponse as Response);

      expect(mockService.blockTransaction).toHaveBeenCalledWith("123", "Suspicious activity");
      expect(mockResponse.json).toHaveBeenCalledWith(updatedMockFraudPrevention);
    });

    it("should return 404 when transaction not found", async () => {
      mockRequest = {
        params: { id: "nonexistent" },
        body: { reason: "Suspicious activity" },
      };

      mockService.blockTransaction.mockResolvedValue(null);

      await fraudPreventionController.blockTransaction(mockRequest as Request, mockResponse as Response);

      expect(mockResponse.status).toHaveBeenCalledWith(404);
      expect(mockResponse.json).toHaveBeenCalledWith({
        message: "Prevención de fraude no encontrada",
      });
    });

    it("should return 400 when reason is missing", async () => {
      mockRequest = {
        params: { id: "123" },
        body: {},
      };

      await fraudPreventionController.blockTransaction(mockRequest as Request, mockResponse as Response);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.json).toHaveBeenCalledWith({
        message: "Se requiere una razón para bloquear la transacción",
      });
    });
  });
});
