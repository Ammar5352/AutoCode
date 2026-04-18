import { useEffect, useRef, useState } from 'react';
import Prism from 'prismjs';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism-tomorrow.css';
import './CodePreview.css';

interface CodePreviewProps {
  code: string;
}

export function CodePreview({ code }: CodePreviewProps) {
  const codeRef = useRef<HTMLElement>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (codeRef.current) {
      Prism.highlightElement(codeRef.current);
    }
  }, [code]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = code;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([code], { type: 'text/x-python' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'autocode_output.py';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const lineCount = code.split('\n').length;

  if (!code) return null;

  return (
    <div className="code-preview" id="code-preview-section">
      {/* Toolbar */}
      <div className="code-toolbar">
        <div className="code-toolbar-left">
          <div className="code-dots">
            <span className="code-dot code-dot--red" />
            <span className="code-dot code-dot--yellow" />
            <span className="code-dot code-dot--green" />
          </div>
          <span className="code-filename">autocode_output.py</span>
          <span className="code-lang-badge">Python</span>
        </div>
        <div className="code-toolbar-right">
          <span className="code-line-count">{lineCount} lines</span>
          <button
            id="copy-code-button"
            className={`code-action-btn ${copied ? 'code-action-btn--success' : ''}`}
            onClick={handleCopy}
            title="Copy to clipboard"
          >
            {copied ? (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
                Copied!
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                </svg>
                Copy
              </>
            )}
          </button>
          <button
            id="download-code-button"
            className="code-action-btn"
            onClick={handleDownload}
            title="Download as .py file"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            Download
          </button>
        </div>
      </div>

      {/* Code Block */}
      <div className="code-scroll-area">
        <div className="code-line-numbers" aria-hidden="true">
          {Array.from({ length: lineCount }, (_, i) => (
            <span key={i + 1} className="code-line-number">
              {i + 1}
            </span>
          ))}
        </div>
        <pre className="code-pre">
          <code ref={codeRef} className="language-python">
            {code}
          </code>
        </pre>
      </div>
    </div>
  );
}
