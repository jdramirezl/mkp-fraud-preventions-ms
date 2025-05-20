import { Request, Response } from "express";
import { FraudPreventionService } from "../services/fraudPreventionService";
import { FraudPreventionEntity } from "../entity/fraudPreventionEntity";

export class FraudPreventionController {
  private fraudPreventionService: FraudPreventionService;

  constructor() {
    this.fraudPreventionService = new FraudPreventionService();
  }

  getAll = async (req: Request, res: Response): Promise<Response> => {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;

      const fraudPreventions = await this.fraudPreventionService.findAll(page, limit);
      return res.status(200).json(fraudPreventions);
    } catch (error) {
      console.error("Error fetching fraud preventions:", error);
      return res.status(500).json({ message: "Error al obtener las prevenciones de fraude" });
    }
  };

  getById = async (req: Request, res: Response): Promise<Response> => {
    try {
      const id = req.params.id;
      const fraudPrevention = await this.fraudPreventionService.findById(id);

      if (!fraudPrevention) {
        return res.status(404).json({ message: "Prevención de fraude no encontrada" });
      }

      return res.status(200).json(fraudPrevention);
    } catch (error) {
      console.error("Error fetching fraud prevention:", error);
      return res.status(500).json({ message: "Error al obtener la prevención de fraude" });
    }
  };

  getByTransactionId = async (req: Request, res: Response): Promise<Response> => {
    try {
      const transactionId = req.params.transactionId;
      const fraudPrevention = await this.fraudPreventionService.findByTransactionId(transactionId);

      if (!fraudPrevention) {
        return res.status(404).json({ message: "Prevención de fraude no encontrada para esta transacción" });
      }

      return res.status(200).json(fraudPrevention);
    } catch (error) {
      console.error("Error fetching fraud prevention by transaction:", error);
      return res.status(500).json({ message: "Error al obtener la prevención de fraude" });
    }
  };

  getByUserId = async (req: Request, res: Response): Promise<Response> => {
    try {
      const userId = req.params.userId;
      const fraudPreventions = await this.fraudPreventionService.findByUserId(userId);
      return res.status(200).json(fraudPreventions);
    } catch (error) {
      console.error("Error fetching fraud preventions by user:", error);
      return res.status(500).json({ message: "Error al obtener las prevenciones de fraude del usuario" });
    }
  };

  create = async (req: Request, res: Response): Promise<Response> => {
    try {
      const fraudPreventionData = req.body as Partial<FraudPreventionEntity>;
      
      // Evaluar el riesgo antes de crear
      if (!fraudPreventionData.riskLevel) {
        fraudPreventionData.riskLevel = await this.fraudPreventionService.assessRisk(fraudPreventionData);
      }
      
      const fraudPrevention = await this.fraudPreventionService.create(fraudPreventionData);
      return res.status(201).json(fraudPrevention);
    } catch (error) {
      console.error("Error creating fraud prevention:", error);
      return res.status(500).json({ message: "Error al crear la prevención de fraude" });
    }
  };

  update = async (req: Request, res: Response): Promise<Response> => {
    try {
      const id = req.params.id;
      const fraudPreventionData = req.body as Partial<FraudPreventionEntity>;

      const updatedFraudPrevention = await this.fraudPreventionService.update(id, fraudPreventionData);

      if (!updatedFraudPrevention) {
        return res.status(404).json({ message: "Prevención de fraude no encontrada" });
      }

      return res.status(200).json(updatedFraudPrevention);
    } catch (error) {
      console.error("Error updating fraud prevention:", error);
      return res.status(500).json({ message: "Error al actualizar la prevención de fraude" });
    }
  };

  delete = async (req: Request, res: Response): Promise<Response> => {
    try {
      const id = req.params.id;
      const deleted = await this.fraudPreventionService.delete(id);

      if (!deleted) {
        return res.status(404).json({ message: "Prevención de fraude no encontrada" });
      }

      return res.status(204).json();
    } catch (error) {
      console.error("Error deleting fraud prevention:", error);
      return res.status(500).json({ message: "Error al eliminar la prevención de fraude" });
    }
  };

  blockTransaction = async (req: Request, res: Response): Promise<Response> => {
    try {
      const id = req.params.id;
      const { reason } = req.body;

      if (!reason) {
        return res.status(400).json({ message: "Se requiere una razón para bloquear la transacción" });
      }

      const blockedFraudPrevention = await this.fraudPreventionService.blockTransaction(id, reason);

      if (!blockedFraudPrevention) {
        return res.status(404).json({ message: "Prevención de fraude no encontrada" });
      }

      return res.status(200).json(blockedFraudPrevention);
    } catch (error) {
      console.error("Error blocking transaction:", error);
      return res.status(500).json({ message: "Error al bloquear la transacción" });
    }
  };
}