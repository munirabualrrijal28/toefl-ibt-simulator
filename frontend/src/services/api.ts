import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const sessionService = {
  startSession: () => api.post('/session/start'),
  getCurrentState: (sessionId: string) => api.get(`/session/${sessionId}/current-state`),
  getNextItem: (sessionId: string) => api.get(`/session/${sessionId}/next-item`),
  submitResponse: (sessionId: string, questionId: string, payload: { text_payload?: string; audio_path?: string }) =>
    api.post(`/session/${sessionId}/submit-response`, {
      question_id: questionId,
      text_payload: payload.text_payload ?? null,
      audio_path: payload.audio_path ?? null,
    }),
  getScore: (sessionId: string) => api.get(`/session/${sessionId}/score`),
};

export default api;
