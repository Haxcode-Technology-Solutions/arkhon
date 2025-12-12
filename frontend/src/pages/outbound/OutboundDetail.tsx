import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { outboundApi } from '@/services';
import PageContainer from '@/components/layout/PageContainer';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import StatusBadge from '@/components/shared/StatusBadge';
import Button from '@/components/shared/Button';
import { ArrowLeft } from 'lucide-react';
import { format } from 'date-fns';

export default function OutboundDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: job, isLoading, error } = useQuery({
    queryKey: ['outbound', id],
    queryFn: () => outboundApi.get(Number(id)),
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;
  if (!job) return <ErrorBanner error={{ message: 'Job not found' }} />;

  return (
    <PageContainer
      title={`Outbound Job #${job.id}`}
      subtitle={job.sync_id}
      action={
        <Button onClick={() => navigate('/outbound')} variant="secondary">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to List
        </Button>
      }
    >
      <div className="space-y-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-sm text-gray-600">Status</p>
              <div className="mt-2">
                <StatusBadge status={job.status} />
              </div>
            </div>
            <div>
              <p className="text-sm text-gray-600">Job Type</p>
              <p className="mt-2 text-lg font-semibold">{job.job_type}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Retry Count</p>
              <p className="mt-2 text-lg font-semibold">
                {job.retry_count} / {job.max_retries}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Statistics</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-sm text-gray-600">Total</p>
              <p className="mt-2 text-2xl font-bold">{job.total_count}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Success</p>
              <p className="mt-2 text-2xl font-bold text-green-600">{job.success_count}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Errors</p>
              <p className="mt-2 text-2xl font-bold text-red-600">{job.error_count}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Timeline</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Created</span>
              <span className="text-sm font-medium">
                {format(new Date(job.created_at), 'MMM d, yyyy HH:mm:ss')}
              </span>
            </div>
            {job.started_at && (
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Started</span>
                <span className="text-sm font-medium">
                  {format(new Date(job.started_at), 'MMM d, yyyy HH:mm:ss')}
                </span>
              </div>
            )}
            {job.completed_at && (
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Completed</span>
                <span className="text-sm font-medium">
                  {format(new Date(job.completed_at), 'MMM d, yyyy HH:mm:ss')}
                </span>
              </div>
            )}
          </div>
        </div>

        {job.message && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold mb-2">Message</h3>
            <p className="text-sm text-gray-700">{job.message}</p>
          </div>
        )}

        {job.bulk_data && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold mb-4">Bulk Data</h3>
            <div className="bg-gray-50 rounded p-4 max-h-96 overflow-auto">
              <pre className="text-xs font-mono text-gray-700 whitespace-pre-wrap">
                {JSON.stringify(JSON.parse(job.bulk_data), null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </PageContainer>
  );
}
