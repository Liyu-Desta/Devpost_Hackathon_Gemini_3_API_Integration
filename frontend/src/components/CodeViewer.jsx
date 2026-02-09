import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check } from 'lucide-react';

/**
 * Code viewer component with syntax highlighting and copy functionality.
 */
export default function CodeViewer({ files }) {
  const [activeFile, setActiveFile] = useState('models.py');
  const [copied, setCopied] = useState(false);

  const fileNames = Object.keys(files || {});

  const getLanguage = (filename) => {
    if (filename.endsWith('.py')) return 'python';
    if (filename.endsWith('.jsx')) return 'jsx';
    if (filename.endsWith('.md')) return 'markdown';
    return 'text';
  };

  const handleCopy = async () => {
    const code = files[activeFile] || '';
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  if (!files || fileNames.length === 0) {
    return (
      <div className="bg-gray-50 rounded-lg p-8 text-center text-gray-500">
        <p>No code files generated yet. Upload an image and generate code first.</p>
      </div>
    );
  }

  return (
    <div className="w-full bg-white rounded-lg shadow-lg overflow-hidden">
      {/* File tabs */}
      <div className="flex border-b border-gray-200 bg-gray-50 overflow-x-auto">
        {fileNames.map((filename) => (
          <button
            key={filename}
            onClick={() => setActiveFile(filename)}
            className={`px-6 py-3 font-medium text-sm whitespace-nowrap transition-colors ${
              activeFile === filename
                ? 'border-b-2 border-indigo-600 text-indigo-600 bg-white'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            {filename}
          </button>
        ))}
      </div>

      {/* Code content */}
      <div className="relative">
        <div className="absolute top-4 right-4 z-10">
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm"
            title="Copy to clipboard"
          >
            {copied ? (
              <>
                <Check size={16} />
                Copied!
              </>
            ) : (
              <>
                <Copy size={16} />
                Copy
              </>
            )}
          </button>
        </div>
        
        <SyntaxHighlighter
          language={getLanguage(activeFile)}
          style={vscDarkPlus}
          customStyle={{
            margin: 0,
            padding: '1.5rem',
            fontSize: '0.875rem',
            minHeight: '400px',
          }}
          showLineNumbers
        >
          {files[activeFile] || ''}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
