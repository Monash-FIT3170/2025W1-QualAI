/**
 * Type definitions for the priority-based highlighting system
 */

export type HighlightPriority = 'HIGH' | 'LOW' | 'IGNORE';

export interface HighlightIndexes {
  index_start: number;
  index_end: number;
}

export interface HighlightData {
  indexes: HighlightIndexes;
  priority: HighlightPriority;
}

export const HIGHLIGHT_COLORS: Record<HighlightPriority, string> = {
  HIGH: '#22c55e',    // green - Tailwind green-500
  LOW: '#fbbf24',  // yellow - Tailwind amber-400
  IGNORE: '#ef4444'   // red - Tailwind red-500
};

export const HIGHLIGHT_PRIORITY_LABELS: Record<HighlightPriority, string> = {
  HIGH: 'High Priority',
  LOW: 'Medium Priority',
  IGNORE: 'Ignore'
};

// Type guard for validation
export function isValidPriority(value: string): value is HighlightPriority {
  return ['HIGH', 'LOW', 'IGNORE'].includes(value);
}

// Document API types
export interface DocumentResponse {
  content: string;
  highlights: HighlightData[];
}

export interface DocumentUpdateRequest {
  content: string;
  highlights: HighlightData[];
}