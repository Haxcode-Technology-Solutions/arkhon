import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { feedsApi } from '@/services';
import PageContainer from '@/components/layout/PageContainer';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import StatusBadge from '@/components/shared/StatusBadge';
import Button from '@/components/shared/Button';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

export default function FeedDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: feed, isLoading, error, refetch } = useQuery({
    queryKey: ['feed', id],
    queryFn: () => feedsApi.get(Number(id)),
  });

  const handleRetry = async () => {
    try {
      await feedsApi.retry(Number(id));
      toast.success('Feed import retry initiated');
      refetch();
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to retry');
    }
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;
  if (!feed) return <ErrorBanner error={{ message: 'Feed not found' }} />;

  return (
    <PageContainer
      title={`Feed #${feed.id}`}
      subtitle={feed.file_name}
      action={
        <div className="flex gap-2">
          {(feed.status === 'failed' || feed.status === 'partial') && (
            <Button onClick={handleRetry} variant="primary" size="sm">
              <RefreshCw className="w-4 h-4 mr-2" />
              Retry Import
            </Button>
          )}
          <Button onClick={() => navigate('/feeds')} variant="secondary" size="sm">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to List
          </Button>
        </div>
      }
    >
      <div className="space-y-6">
        {/* Status and Stats */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
              <p className="text-sm text-gray-600">Status</p>
              <div className="mt-2">
                <StatusBadge status={feed.status} />
              </div>
            </div>
            <div>
              <p className="text-sm text-gray-600">Entity</p>
              <p className="mt-2 text-lg font-semibold">{feed.entity_code}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Records</p>
              <p className="mt-2 text-lg font-semibold">{feed.total_count.toLocaleString()}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">File Size</p>
              <p className="mt-2 text-lg font-semibold">
                {feed.file_size ? `${(feed.file_size / 1024 / 1024).toFixed(2)} MB` : 'N/A'}
              </p>
            </div>
          </div>
        </div>

        {/* Processing Stats */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Processing Statistics</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-sm text-gray-600">Success</p>
              <p className="mt-2 text-2xl font-bold text-green-600">
                {feed.success_count.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Errors</p>
              <p className="mt-2 text-2xl font-bold text-red-600">
                {feed.error_count.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Pending</p>
              <p className="mt-2 text-2xl font-bold text-yellow-600">
                {feed.pending_count.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        {/* Timeline */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Timeline</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Created</span>
              <span className="text-sm font-medium">
                {format(new Date(feed.created_at), 'MMM d, yyyy HH:mm:ss')}
              </span>
            </div>
            {feed.started_at && (
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Started</span>
                <span className="text-sm font-medium">
                  {format(new Date(feed.started_at), 'MMM d, yyyy HH:mm:ss')}
                </span>
              </div>
            )}
            {feed.completed_at && (
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Completed</span>
                <span className="text-sm font-medium">
                  {format(new Date(feed.completed_at), 'MMM d, yyyy HH:mm:ss')}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Error Message */}
        {feed.error_message && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-red-900 mb-2">Error Message</h3>
            <p className="text-sm text-red-700">{feed.error_message}</p>
          </div>
        )}

        {/* Logs */}
        {feed.processing_logs && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold mb-4">Processing Logs</h3>
            <div className="bg-gray-50 rounded p-4 max-h-96 overflow-auto">
              <pre className="text-xs font-mono text-gray-700 whitespace-pre-wrap">
                {JSON.stringify(JSON.parse(feed.processing_logs), null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </PageContainer>
  );
}
