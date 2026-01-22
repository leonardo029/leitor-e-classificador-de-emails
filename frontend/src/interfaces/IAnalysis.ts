export interface IKeywordAnalysis {
  matched_keywords: string[];
  produtivo_score: number;
  improdutivo_score: number;
  total_keywords: number;
}

export interface IProcessingDetails {
  classification_method: 'keywords_only' | 'ai' | 'fallback';
  used_full_text?: boolean | null;
  used_ai?: boolean | null;
  used_fallback?: boolean | null;
  keyword_analysis: IKeywordAnalysis;
}

export interface INlpDebug {
  detected_keywords: string;
  keyword_analysis?: IKeywordAnalysis | null;
}

export interface IAnalysisResult {
  filename?: string | null;
  category: 'Produtivo' | 'Improdutivo';
  confidence_score: number;
  summary: string;
  reason?: string | null;
  suggested_response: string | null;
  nlp_debug?: INlpDebug;
  processing_details?: IProcessingDetails;
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
