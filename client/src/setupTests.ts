// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import "@testing-library/jest-dom/vitest";
import { vi, beforeEach, afterAll } from "vitest";

// Polyfill jest globals for Vitest compatibility (tests use jest.fn, jest.spyOn etc.)
Object.defineProperty(globalThis, "jest", {
  value: {
    fn: vi.fn,
    spyOn: vi.spyOn,
    clearAllMocks: vi.clearAllMocks,
    resetAllMocks: vi.resetAllMocks,
  },
  writable: true,
  configurable: true,
});

// Vitest shares mocks across test files unlike Jest. Clear all mocks between
// tests to prevent spy count contamination.
beforeEach(() => {
  vi.clearAllMocks();
  vi.restoreAllMocks();
});

afterAll(() => {
  vi.resetModules();
});
