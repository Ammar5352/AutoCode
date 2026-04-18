import './Header.css';

export function Header() {
  return (
    <header className="header" id="app-header">
      <div className="header-inner">
        <div className="header-brand">
          <div className="header-logo">
            <span className="header-logo-icon">⚡</span>
          </div>
          <div className="header-text">
            <h1 className="header-title">AutoCode AI</h1>
            <span className="header-tagline">AI-Powered Code Generation</span>
          </div>
        </div>
        <div className="header-badge">
          <span className="header-badge-dot" />
          <span className="header-badge-text">Online</span>
        </div>
      </div>
    </header>
  );
}
