import { useState } from 'react';
import { CodePreview } from './CodePreview';
import { SummaryCard } from './SummaryCard';
import { FeedbackCard } from './FeedbackCard';
import './TabSwitcher.css';

interface TabSwitcherProps {
  code: string;
  summary: string;
  feedback: string;
}

type TabKey = 'code' | 'summary' | 'feedback';

interface Tab {
  key: TabKey;
  label: string;
  icon: string;
  count?: number;
}

export function TabSwitcher({ code, summary, feedback }: TabSwitcherProps) {
  const [activeTab, setActiveTab] = useState<TabKey>('code');

  const tabs: Tab[] = [
    { key: 'code', label: 'Code', icon: '🔤' },
    { key: 'summary', label: 'Summary', icon: '📋' },
    { key: 'feedback', label: 'Feedback', icon: '💡' },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'code':
        return <CodePreview code={code} />;
      case 'summary':
        return <SummaryCard summary={summary} />;
      case 'feedback':
        return <FeedbackCard feedback={feedback} />;
    }
  };

  // Hide if no data at all
  if (!code && !summary && !feedback) return null;

  return (
    <div className="tab-switcher card animate-fade-in-up" id="tab-switcher-section">
      <div className="tab-header">
        <div className="tab-list" role="tablist">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              id={`tab-${tab.key}`}
              className={`tab-button ${activeTab === tab.key ? 'tab-button--active' : ''}`}
              onClick={() => setActiveTab(tab.key)}
              role="tab"
              aria-selected={activeTab === tab.key}
              aria-controls={`panel-${tab.key}`}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div
        className="tab-content"
        id={`panel-${activeTab}`}
        role="tabpanel"
        aria-labelledby={`tab-${activeTab}`}
      >
        {renderContent()}
      </div>
    </div>
  );
}
