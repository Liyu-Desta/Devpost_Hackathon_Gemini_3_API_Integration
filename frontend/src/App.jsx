import React, { useState, useEffect } from 'react';
import { Sparkles, AlertCircle } from 'lucide-react';
import ImageUpload from './components/ImageUpload';
import CodeViewer from './components/CodeViewer';
import Preview from './components/Preview';
import Tabs from './components/Tabs';
import LoadingSpinner from './components/LoadingSpinner';
import ExampleSelector from './components/ExampleSelector';
import { analyzeImage, getExamples, getExample } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('input');
  const [selectedImage, setSelectedImage] = useState(null);
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [examples, setExamples] = useState([]);
  const [result, setResult] = useState(null);

  // Load examples on mount
  useEffect(() => {
    const loadExamples = async () => {
      try {
        const exampleList = await getExamples();
        setExamples(exampleList);
      } catch (err) {
        console.error('Failed to load examples:', err);
      }
    };
    loadExamples();
  }, []);

  const handleGenerate = async () => {
    if (!selectedImage) {
      setError('Please upload an image first');
      return;
    }

    if (!description.trim()) {
      setError('Please provide a description');
      return;
    }

    setLoading(true);
    setError(null);
    setActiveTab('code');

    try {
      const response = await analyzeImage(selectedImage, description);
      setResult(response);
      setActiveTab('code');
    } catch (err) {
      setError(err.message || 'Failed to generate code. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleSelect = async (exampleId) => {
    setLoading(true);
    setError(null);
    setActiveTab('code');

    try {
      const response = await getExample(exampleId);
      setResult(response);
      setActiveTab('code');
    } catch (err) {
      setError(err.message || 'Failed to load example');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="text-indigo-600" size={40} />
            <h1 className="text-5xl font-bold text-gray-900">SPATIALCODE</h1>
          </div>
          <p className="text-xl text-gray-600">
            Transform your sketches and images into full-stack applications
          </p>
        </header>

        {/* Tabs */}
        <Tabs activeTab={activeTab} onTabChange={setActiveTab} />

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
            <div>
              <p className="text-red-800 font-medium">Error</p>
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow-xl p-6 md:p-8">
          {activeTab === 'input' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                  Upload Your Image
                </h2>
                <ImageUpload
                  onImageSelect={handleImageSelect}
                  selectedImage={selectedImage}
                />
              </div>

              <div>
                <label
                  htmlFor="description"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Description (max 200 characters)
                </label>
                <textarea
                  id="description"
                  value={description}
                  onChange={(e) => {
                    setDescription(e.target.value);
                    setError(null);
                  }}
                  maxLength={200}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
                  placeholder="Describe what kind of application you want to generate..."
                />
                <p className="mt-2 text-sm text-gray-500">
                  {description.length}/200 characters
                </p>
              </div>

              <button
                onClick={handleGenerate}
                disabled={loading || !selectedImage || !description.trim()}
                className="w-full py-3 px-6 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles size={20} />
                    Generate Code
                  </>
                )}
              </button>

              <ExampleSelector
                examples={examples}
                onSelectExample={handleExampleSelect}
                loading={loading}
              />
            </div>
          )}

          {activeTab === 'code' && (
            <div>
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">
                Generated Code
              </h2>
              {loading ? (
                <LoadingSpinner message="Generating your code..." />
              ) : result ? (
                <CodeViewer files={result.generated_files} />
              ) : (
                <div className="bg-gray-50 rounded-lg p-8 text-center text-gray-500">
                  <p>No code generated yet. Go to the Input tab to get started.</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'preview' && (
  result ? (
    <Preview generatedFiles={result.generated_files} />
  ) : (
    <div className="bg-gray-50 rounded-lg p-8 text-center text-gray-500">
      No preview available. Generate code first.
    </div>
  )
)}


          {activeTab === 'analysis' && (
            <div>
              <h2 className="text-2xl font-semibold text-gray-800 mb-6">
                AI Analysis Summary
              </h2>
              {loading ? (
                <LoadingSpinner message="Analyzing..." />
              ) : result ? (
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
                  <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                    {result.analysis_summary}
                  </p>
                </div>
              ) : (
                <div className="bg-gray-50 rounded-lg p-8 text-center text-gray-500">
                  <p>No analysis available yet. Generate code first.</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>Built with FastAPI, React, and Gemini Vision API</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
