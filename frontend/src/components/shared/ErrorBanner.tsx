import { AlertCircle, X } from 'lucide-react';
import { useState } from 'react';

interface ErrorBannerProps {
  error: any;
  onDismiss?: () => void;
}

export default function ErrorBanner({ error, onDismiss }: ErrorBannerProps) {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  const errorMessage =
    error?.response?.data?.detail ||
    error?.message ||
    'An unexpected error occurred';

  const handleDismiss = () => {
    setDismissed(true);
    onDismiss?.();
  };

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <div className="flex items-start">
        <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium text-red-800">Error</h3>
          <p className="mt-1 text-sm text-red-700">{errorMessage}</p>
        </div>
        {onDismiss && (
          <button
            onClick={handleDismiss}
            className="ml-3 text-red-600 hover:text-red-800"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
}
