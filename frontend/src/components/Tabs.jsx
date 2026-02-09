import React from 'react';
import { Upload, Code, FileText, Eye } from 'lucide-react';

/**
 * Tab navigation component.
 */
export default function Tabs({ activeTab, onTabChange }) {
  const tabs = [
    { id: 'input', label: 'Input', icon: Upload },
    { id: 'code', label: 'Generated Code', icon: Code },
    { id: 'preview', label: 'Preview', icon: Eye },
    { id: 'analysis', label: 'Analysis', icon: FileText },
  ];

  return (
    <div className="flex border-b border-gray-300 mb-6 overflow-x-auto">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        return (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex items-center gap-2 px-6 py-3 font-semibold transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-600 hover:text-indigo-600'
            }`}
          >
            <Icon size={20} />
            {tab.label}
          </button>
        );
      })}
    </div>
  );
}
