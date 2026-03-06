export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: { source: string; excerpt: string; score: number }[];
  confidence?: number;
  lowConfidence?: boolean;
  streaming?: boolean;
  logId?: string | null;
  feedbackEnabled?: boolean;
  isPositive?: boolean | null;
  submitting?: boolean;
  feedbackError?: string | null;
  comment?: string;
  showComment?: boolean;
}
