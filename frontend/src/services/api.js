/** API service for communicating with the backend. */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Analyze an image and generate code.
 * @param {File} imageFile - The image file to analyze
 * @param {string} description - Text description (max 200 chars)
 * @returns {Promise<Object>} Analysis result with generated files
 */
export const analyzeImage = async (imageFile, description) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('description', description);

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to analyze image');
  }

  return response.json();
};

/**
 * Get list of available examples.
 * @returns {Promise<string[]>} List of example IDs
 */
export const getExamples = async () => {
  const response = await fetch(`${API_BASE_URL}/examples`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch examples');
  }

  return response.json();
};

/**
 * Get a specific example by ID.
 * @param {string} exampleId - Example identifier
 * @returns {Promise<Object>} Example data with generated files
 */
export const getExample = async (exampleId) => {
  const response = await fetch(`${API_BASE_URL}/examples/${exampleId}`);
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch example');
  }

  return response.json();
};
