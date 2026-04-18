import { useState, type FormEvent, type KeyboardEvent } from 'react';
import './ChatInput.css';

interface ChatInputProps {
  onSubmit: (message: string) => void;
  loading: boolean;
  onHintClick?: (hint: string) => void;
}

export function ChatInput({ onSubmit, loading }: ChatInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim() && !loading) {
      onSubmit(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-input-wrapper" id="chat-input-section">
      <form className="chat-input-container" onSubmit={handleSubmit}>
        <div className="chat-input-inner">
          <textarea
            id="task-input"
            className="chat-input-field"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your coding task... (e.g., build a FastAPI CRUD app)"
            rows={1}
            disabled={loading}
            autoFocus
          />
          <button
            type="submit"
            id="submit-button"
            className={`chat-input-submit ${loading ? 'chat-input-submit--loading' : ''}`}
            disabled={!input.trim() || loading}
            aria-label="Submit task"
          >
            {loading ? (
              <span className="chat-input-spinner" />
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            )}
          </button>
        </div>
        <div className="chat-input-hint">
          Press <kbd>Enter</kbd> to send · <kbd>Shift + Enter</kbd> for new line
        </div>
      </form>
    </div>
  );
}
