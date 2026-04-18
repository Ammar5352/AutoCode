import { Header } from './components/Header';
import { ChatInput } from './components/ChatInput';
import { LoadingState } from './components/LoadingState';
import { ResponseCard } from './components/ResponseCard';
import { TabSwitcher } from './components/TabSwitcher';
import { useAutoCode } from './hooks/useAutoCode';
import './App.css';

const EXAMPLE_HINTS = [
  'Build a FastAPI CRUD app',
  'Create a Flask REST API',
  'Write a web scraper',
  'Build a CLI tool with Click',
];

function App() {
  const { response, loading, error, submitTask } = useAutoCode();

  const hasResponse = response !== null;
  const showWelcome = !loading && !hasResponse && !error;

  return (
    <div className="app" id="app-root">
      <Header />

      <main className="app-content">
        {/* Welcome State */}
        {showWelcome && (
          <div className="welcome-container">
            <div className="welcome-icon">⚡</div>
            <h2 className="welcome-title">What would you like to build?</h2>
            <p className="welcome-subtitle">
              Describe your coding task and AutoCode AI will generate, review,
              and optimize production-ready Python code for you.
            </p>
            <div className="welcome-hints">
              {EXAMPLE_HINTS.map((hint) => (
                <button
                  key={hint}
                  className="welcome-hint"
                  onClick={() => submitTask(hint)}
                >
                  {hint}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && <LoadingState />}

        {/* Error State */}
        {error && (
          <div className="card error-card animate-fade-in" id="error-section">
            <div className="card-header">
              <div className="card-icon">⚠️</div>
              <div>
                <div className="card-title">Something went wrong</div>
                <div className="card-label">Error</div>
              </div>
            </div>
            <p className="error-text">{error}</p>
          </div>
        )}

        {/* Response Sections */}
        {hasResponse && (
          <div className="section-gap animate-slide-up">
            <ResponseCard response={response.response} />
            <TabSwitcher
              code={response.task_code}
              summary={response.summary}
              feedback={response.feedback}
            />
          </div>
        )}
      </main>

      <ChatInput onSubmit={submitTask} loading={loading} />
    </div>
  );
}

export default App;
