import React, { useState } from 'react';
import { Upload, X, Image as ImageIcon } from 'lucide-react';

/**
 * Image upload component with preview.
 */
export default function ImageUpload({ onImageSelect, selectedImage }) {
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      onImageSelect(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleRemove = () => {
    onImageSelect(null);
    setPreview(null);
  };

  return (
    <div className="w-full">
      {preview ? (
        <div className="relative w-full">
          <img
            src={preview}
            alt="Preview"
            className="w-full h-64 object-contain border-2 border-gray-300 rounded-lg bg-gray-50"
          />
          <button
            onClick={handleRemove}
            className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 transition-colors"
            aria-label="Remove image"
          >
            <X size={20} />
          </button>
        </div>
      ) : (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? 'border-indigo-500 bg-indigo-50'
              : 'border-gray-300 hover:border-indigo-400'
          }`}
        >
          <input
            type="file"
            accept="image/*"
            onChange={handleChange}
            className="hidden"
            id="image-upload"
          />
          <label
            htmlFor="image-upload"
            className="cursor-pointer flex flex-col items-center gap-4"
          >
            <div className="p-4 bg-indigo-100 rounded-full">
              <ImageIcon size={32} className="text-indigo-600" />
            </div>
            <div>
              <p className="text-gray-700 font-medium">
                Click to upload or drag and drop
              </p>
              <p className="text-gray-500 text-sm mt-1">
                PNG, JPG, GIF up to 10MB
              </p>
            </div>
            <button
              type="button"
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center gap-2"
            >
              <Upload size={18} />
              Choose Image
            </button>
          </label>
        </div>
      )}
    </div>
  );
}
