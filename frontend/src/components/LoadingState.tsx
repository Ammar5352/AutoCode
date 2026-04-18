import './LoadingState.css';

export function LoadingState() {
  return (
    <div className="loading-container animate-fade-in" id="loading-indicator">
      <div className="loading-card card">
        <div className="loading-visual">
          <div className="loading-rings">
            <div className="loading-ring loading-ring--outer" />
            <div className="loading-ring loading-ring--inner" />
            <div className="loading-core">
              <span>⚡</span>
            </div>
          </div>
        </div>
        <div className="loading-text">
          <h3 className="loading-title">Generating Code</h3>
          <p className="loading-description">
            AI agents are writing, reviewing, and optimizing your code...
          </p>
        </div>
        <div className="loading-steps">
          <div className="loading-step loading-step--active">
            <span className="loading-step-dot" />
            <span>Analyzing task</span>
          </div>
          <div className="loading-step loading-step--pending">
            <span className="loading-step-dot" />
            <span>Writing code</span>
          </div>
          <div className="loading-step loading-step--pending">
            <span className="loading-step-dot" />
            <span>Reviewing &amp; optimizing</span>
          </div>
        </div>
      </div>
    </div>
  );
}
