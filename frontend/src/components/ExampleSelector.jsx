import React from 'react';
import { Sparkles } from 'lucide-react';

/**
 * Example selector component for pre-built demos.
 */
export default function ExampleSelector({ examples, onSelectExample, loading }) {
  const exampleLabels = {
    'food-pantry': '🥫 Food Pantry Management',
    'library': '📚 Library Book Tracking',
    'clinic': '🏥 Clinic Appointment System',
  };

  return (
    <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6 border border-purple-200">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="text-purple-600" size={20} />
        <h3 className="font-semibold text-gray-800">Try Pre-built Examples</h3>
      </div>
      <p className="text-sm text-gray-600 mb-4">
        Explore these pre-generated examples without uploading an image:
      </p>
      <div className="flex flex-wrap gap-3">
        {examples.map((exampleId) => (
          <button
            key={exampleId}
            onClick={() => onSelectExample(exampleId)}
            disabled={loading}
            className="px-4 py-2 bg-white border border-purple-300 rounded-lg hover:bg-purple-50 hover:border-purple-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium text-gray-700"
          >
            {exampleLabels[exampleId] || exampleId}
          </button>
        ))}
      </div>
    </div>
  );
}
