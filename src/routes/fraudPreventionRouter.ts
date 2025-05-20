import { Router } from "express";
import { FraudPreventionController } from "../controllers/fraudPreventionController";

export const fraudPreventionRouter = Router();
const fraudPreventioController = new FraudPreventionController();

/**
 * @route   GET /api/fraud-preventions
 * @desc    Get all fraud preventions with pagination
 */
fraudPreventionRouter.get("/", fraudPreventioController.getAll);

/**
 * @route   GET /api/fraud-preventions/:id
 * @desc    Get a fraud prevention by ID
 */
fraudPreventionRouter.get("/:id", fraudPreventioController.getById);

/**
 * @route   GET /api/fraud-preventions/transaction/:transactionId
 * @desc    Get a fraud prevention by transaction ID
 */
fraudPreventionRouter.get("/transaction/:transactionId", fraudPreventioController.getByTransactionId);

/**
 * @route   GET /api/fraud-preventions/user/:userId
 * @desc    Get all fraud preventions for a specific user
 */
fraudPreventionRouter.get("/user/:userId", fraudPreventioController.getByUserId);

/**
 * @route   POST /api/fraud-preventions
 * @desc    Create a new fraud prevention record
 */
fraudPreventionRouter.post("/", fraudPreventioController.create);

/**
 * @route   PUT /api/fraud-preventions/:id
 * @desc    Update a fraud prevention record
 */
fraudPreventionRouter.put("/:id", fraudPreventioController.update);

/**
 * @route   DELETE /api/fraud-preventions/:id
 * @desc    Delete a fraud prevention record
 */
fraudPreventionRouter.delete("/:id", fraudPreventioController.delete);

/**
 * @route   POST /api/fraud-preventions/:id/block
 * @desc    Block a transaction with a specific reason
 */
fraudPreventionRouter.post("/:id/block", fraudPreventioController.blockTransaction);

