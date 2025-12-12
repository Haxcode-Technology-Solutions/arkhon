interface StatusBadgeProps {
  status: string;
  variant?: 'default' | 'feed' | 'job';
}

export default function StatusBadge({ status, variant = 'default' }: StatusBadgeProps) {
  const getStatusColor = () => {
    const statusLower = status.toLowerCase();

    if (statusLower === 'completed' || statusLower === 'success') {
      return 'bg-green-100 text-green-800';
    }
    if (statusLower === 'pending') {
      return 'bg-yellow-100 text-yellow-800';
    }
    if (statusLower === 'processing' || statusLower === 'retrying') {
      return 'bg-blue-100 text-blue-800';
    }
    if (statusLower === 'failed' || statusLower === 'error') {
      return 'bg-red-100 text-red-800';
    }
    if (statusLower === 'partial') {
      return 'bg-orange-100 text-orange-800';
    }
    return 'bg-gray-100 text-gray-800';
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor()}`}
    >
      {status}
    </span>
  );
}
