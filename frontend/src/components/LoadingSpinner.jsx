import React from 'react';
import { Loader2 } from 'lucide-react';

/**
 * Loading spinner component.
 */
export default function LoadingSpinner({ message = 'Processing...' }) {
  return (
    <div className="flex flex-col items-center justify-center p-12">
      <Loader2 className="animate-spin text-indigo-600" size={48} />
      <p className="mt-4 text-gray-600 font-medium">{message}</p>
      <p className="mt-2 text-sm text-gray-500">This may take a few moments</p>
    </div>
  );
}
