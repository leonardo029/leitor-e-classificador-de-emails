export interface INlpDebug {
  detected_keywords: string;
}

export interface IAnalysisResult {
  filename?: string;
  category: 'Produtivo' | 'Improdutivo';
  confidence_score: number;
  summary: string;
  suggested_response: string | null;
  nlp_debug?: INlpDebug;
  processedAt?: string;
}

export interface IApiResponse {
  status: string;
  data: IAnalysisResult;
}

export interface IApiError {
  status: string;
  error_code: string;
  message: string;
  details?: Record<string, unknown>;
}
