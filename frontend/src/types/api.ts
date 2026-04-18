export interface AutoCodeRequest {
  user_message: string;
}

export interface APIResponse {
  response: string;
  task_code: string;
  summary: string;
  feedback: string;
}
