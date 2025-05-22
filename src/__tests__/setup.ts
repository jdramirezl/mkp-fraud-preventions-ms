import { AppDataSource } from '../datasource/datasource';

beforeAll(async () => {
  // Mock the database connection
  jest.spyOn(AppDataSource, 'initialize').mockResolvedValue(AppDataSource);
  jest.spyOn(AppDataSource, 'getRepository').mockReturnValue({
    find: jest.fn(),
    findOne: jest.fn(),
    save: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
  } as any);
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