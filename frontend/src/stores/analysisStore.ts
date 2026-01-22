import type { IAnalysisResult, IApiError, IApiResponse } from '@/interfaces/IAnalysis';
import axios from 'axios';
import { defineStore } from 'pinia';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const ERROR_MESSAGES: Record<string, string> = {
  'INVALID_FILE': 'Arquivo inválido. Use apenas arquivos PDF ou TXT (máximo 10MB).',
  'INVALID_TEXT': 'Texto inválido ou muito longo (máximo 50.000 caracteres).',
  'AI_API_ERROR': 'Erro no serviço de classificação. Tente novamente em alguns instantes.',
  'NLP_PROCESSING_ERROR': 'Erro ao processar o texto. Tente novamente.',
  'CLASSIFIER_ERROR': 'Erro interno do classificador. Tente novamente.',
};

export const useAnalysisStore = defineStore('analysis', {
  state: () => ({
    results: [] as IAnalysisResult[],
    isLoading: false,
    error: null as string | null,
  }),

  actions: {
    loadFromSession() {
      const stored = sessionStorage.getItem('analysis_history');
      if (stored) {
        try {
          this.results = JSON.parse(stored);
        } catch (e) {
          console.error('Erro ao carregar histórico:', e);
          sessionStorage.removeItem('analysis_history');
        }
      }
    },

    saveToSession() {
      try {
        sessionStorage.setItem('analysis_history', JSON.stringify(this.results));
      } catch (e) {
        console.error('Erro ao salvar histórico:', e);
      }
    },

    clearHistory() {
      this.results = [];
      sessionStorage.removeItem('analysis_history');
      this.error = null;
    },

    async analyzeContent(payload: File | string, type: 'file' | 'text') {
      this.isLoading = true;
      this.error = null;

      try {
        let response;

        const formData = new FormData();
        
        if (type === 'file') {
          formData.append('file', payload as File);
        } else {
          formData.append('text', payload as string);
        }
        
        response = await axios.post<IApiResponse>(`${API_URL}/api/v1/process`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        const result: IAnalysisResult = {
          ...response.data.data,
          processedAt: new Date().toISOString()
        };

        this.results.unshift(result);
        this.saveToSession();

      } catch (err: unknown) {
        console.error(err);

        if (axios.isAxiosError(err) && err.response) {
          const errorData = err.response.data as IApiError;
          const errorCode = errorData?.error_code;
          const errorMessage = errorData?.message;

          this.error = ERROR_MESSAGES[errorCode || ''] || errorMessage || 'Erro ao processar solicitação.';
        } else if (axios.isAxiosError(err) && err.request) {
          this.error = 'Erro de conexão. Verifique sua internet e tente novamente.';
        } else {
          this.error = 'Ocorreu um erro inesperado. Tente novamente.';
        }
      } finally {
        this.isLoading = false;
      }
    }
  }
});
