import './SummaryCard.css';

interface SummaryCardProps {
  summary: string;
}

export function SummaryCard({ summary }: SummaryCardProps) {
  if (!summary) return null;

  // Parse summary into structured lines
  const lines = summary
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.length > 0);

  return (
    <div className="summary-card" id="summary-section">
      <div className="summary-items">
        {lines.map((line, index) => {
          // Detect bullet-like lines
          const isBullet =
            line.startsWith('-') ||
            line.startsWith('•') ||
            line.startsWith('*') ||
            /^\d+[.)]\s/.test(line);

          const cleanLine = isBullet
            ? line.replace(/^[-•*]\s*/, '').replace(/^\d+[.)]\s*/, '')
            : line;

          return (
            <div
              key={index}
              className={`summary-item ${isBullet ? 'summary-item--bullet' : 'summary-item--paragraph'}`}
            >
              {isBullet && <span className="summary-bullet">▸</span>}
              <span className="summary-item-text">{cleanLine}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
