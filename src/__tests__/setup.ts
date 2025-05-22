import { AppDataSource } from '../datasource/datasource';

beforeAll(async () => {
  // Mock the database connection
  jest.spyOn(AppDataSource, 'initialize').mockResolvedValue(AppDataSource);
});

afterAll(async () => {
  // Clean up mocks
  jest.restoreAllMocks();
}); 