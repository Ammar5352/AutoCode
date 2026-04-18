import './ResponseCard.css';

interface ResponseCardProps {
  response: string;
}

export function ResponseCard({ response }: ResponseCardProps) {
  if (!response) return null;

  return (
    <div className="response-card card animate-fade-in-up" id="response-section">
      <div className="card-header">
        <div className="card-icon response-icon">💬</div>
        <div>
          <div className="card-title">Response</div>
          <div className="card-label">AI Analysis</div>
        </div>
      </div>
      <p className="response-text">{response}</p>
    </div>
  );
}
