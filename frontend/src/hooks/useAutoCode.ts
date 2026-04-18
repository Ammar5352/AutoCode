import { useState, useCallback } from 'react';
import type { APIResponse } from '../types/api';
import { sendTask } from '../services/api';

interface UseAutoCodeReturn {
  response: APIResponse | null;
  loading: boolean;
  error: string | null;
  submitTask: (message: string) => Promise<void>;
  clearResponse: () => void;
}

export function useAutoCode(): UseAutoCodeReturn {
  const [response, setResponse] = useState<APIResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submitTask = useCallback(async (message: string) => {
    if (!message.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const data = await sendTask(message);
      setResponse(data);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResponse = useCallback(() => {
    setResponse(null);
    setError(null);
  }, []);

  return { response, loading, error, submitTask, clearResponse };
}
