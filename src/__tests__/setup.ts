import { AppDataSource } from '../datasource/datasource';
import { Repository } from 'typeorm';
import { FraudPreventionEntity } from '../entity/fraudPreventionEntity';

// Mock data store
const mockDataStore: { [key: string]: any } = {};

beforeAll(async () => {
  // Mock the database connection
  jest.spyOn(AppDataSource, 'initialize').mockResolvedValue(AppDataSource);
  
  // Create a more sophisticated mock repository
  const mockRepository = {
    find: jest.fn().mockImplementation(async () => Object.values(mockDataStore)),
    findOne: jest.fn().mockImplementation(async (options: any) => {
      const id = options?.where?.id || options;
      return mockDataStore[id] || null;
    }),
    save: jest.fn().mockImplementation(async (entity: any) => {
      const id = entity.id || Math.random().toString(36).substring(7);
      const savedEntity = { ...entity, id };
      mockDataStore[id] = savedEntity;
      return savedEntity;
    }),
    create: jest.fn().mockImplementation((entity: any) => entity),
    update: jest.fn().mockImplementation(async (id: string, updates: any) => {
      if (mockDataStore[id]) {
        mockDataStore[id] = { ...mockDataStore[id], ...updates };
        return { affected: 1 };
      }
      return { affected: 0 };
    }),
    delete: jest.fn().mockImplementation(async (id: string) => {
      if (mockDataStore[id]) {
        delete mockDataStore[id];
        return { affected: 1 };
      }
      return { affected: 0 };
    }),
    count: jest.fn().mockImplementation(async () => Object.keys(mockDataStore).length),
  };

  jest.spyOn(AppDataSource, 'getRepository').mockReturnValue(mockRepository as unknown as Repository<FraudPreventionEntity>);
});

beforeEach(() => {
  // Clear mock data store before each test
  Object.keys(mockDataStore).forEach(key => delete mockDataStore[key]);
});

afterAll(async () => {
  // Clean up mocks
  jest.restoreAllMocks();
});

// Add a dummy test to satisfy Jest's requirement
describe('Setup', () => {
  it('should set up the test environment', () => {
    expect(AppDataSource.initialize).toBeDefined();
  });
}); 