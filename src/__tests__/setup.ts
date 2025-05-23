import { AppDataSource } from '../datasource/datasource';
import { Repository } from 'typeorm';
import { FraudPreventionEntity } from '../entity/fraudPreventionEntity';

beforeAll(async () => {
  // Basic mock repository with minimal implementation
  const mockRepository = {
    find: jest.fn().mockResolvedValue([]),
    findOne: jest.fn().mockResolvedValue(null),
    save: jest.fn().mockImplementation(async (entity) => ({ 
      ...entity, 
      id: 'mock-id' 
    })),
    create: jest.fn().mockImplementation((entity) => entity),
  };

  // Mock the database connection
  jest.spyOn(AppDataSource, 'initialize').mockResolvedValue(AppDataSource);
  jest.spyOn(AppDataSource, 'getRepository').mockReturnValue(mockRepository as unknown as Repository<FraudPreventionEntity>);
});

afterAll(async () => {
  jest.restoreAllMocks();
});

// Add a dummy test to satisfy Jest's requirement
describe('Setup', () => {
  it('should set up the test environment', () => {
    expect(AppDataSource.initialize).toBeDefined();
  });
}); 