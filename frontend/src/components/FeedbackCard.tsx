import './FeedbackCard.css';

interface FeedbackCardProps {
  feedback: string;
}

export function FeedbackCard({ feedback }: FeedbackCardProps) {
  if (!feedback) return null;

  const items = feedback
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .map((line) =>
      line
        .replace(/^[-•*]\s*/, '')
        .replace(/^\d+[.)]\s*/, '')
    );

  return (
    <div className="feedback-card" id="feedback-section">
      <div className="feedback-items">
        {items.map((item, index) => (
          <div key={index} className="feedback-item">
            <div className="feedback-item-icon">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
            </div>
            <span className="feedback-item-text">{item}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
