import type { AutoCodeRequest, APIResponse } from '../types/api';

const API_BASE_URL = 'http://localhost:8081';

export async function sendTask(userMessage: string): Promise<APIResponse> {
  const payload: AutoCodeRequest = { user_message: userMessage };

  const response = await fetch(`${API_BASE_URL}/autocodeai/autocode_agent`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `API error (${response.status}): ${errorText || response.statusText}`
    );
  }

  const data: APIResponse = await response.json();
  return data;
}
