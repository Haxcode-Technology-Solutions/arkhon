import { useQuery, useMutation } from '@tanstack/react-query';
import { cronApi } from '@/services';
import PageContainer from '@/components/layout/PageContainer';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import Button from '@/components/shared/Button';
import { Play, Clock } from 'lucide-react';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';

export default function CronMonitor() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['cron-status'],
    queryFn: () => cronApi.getStatus(),
  });

  const runTaskMutation = useMutation({
    mutationFn: (taskName: string) => cronApi.runTask(taskName),
    onSuccess: (data: any) => {
      toast.success(`Task '${data.task_name}' triggered successfully`);
      refetch();
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Failed to trigger task');
    },
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <PageContainer
      title="Cron Monitor"
      subtitle="Monitor and manage scheduled tasks"
    >
      <div className="space-y-6">
        {/* Worker Status */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Worker Status</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-sm text-gray-600">Status</p>
              <p className="mt-2 text-lg font-semibold">
                <span className={data?.worker_status?.active ? 'text-green-600' : 'text-red-600'}>
                  {data?.worker_status?.active ? 'Active' : 'Inactive'}
                </span>
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Workers</p>
              <p className="mt-2 text-lg font-semibold">{data?.worker_status?.workers}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Pending Tasks</p>
              <p className="mt-2 text-lg font-semibold text-yellow-600">
                {data?.worker_status?.pending_tasks}
              </p>
            </div>
          </div>
        </div>

        {/* Scheduled Tasks */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Scheduled Tasks</h3>
          <div className="space-y-4">
            {data?.tasks?.map((task: any) => (
              <div
                key={task.name}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{task.description}</h4>
                    <div className="mt-2 space-y-1 text-sm">
                      <div className="flex items-center text-gray-600">
                        <Clock className="w-4 h-4 mr-2" />
                        <span>Schedule: <code className="font-mono">{task.schedule}</code></span>
                      </div>
                      {task.last_run && (
                        <div className="text-gray-600">
                          Last run:{' '}
                          {formatDistanceToNow(new Date(task.last_run), { addSuffix: true })}
                          {' '}
                          <span className={`ml-2 text-xs px-2 py-0.5 rounded ${
                            task.last_status === 'success'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {task.last_status}
                          </span>
                        </div>
                      )}
                      {task.next_run && (
                        <div className="text-gray-600">
                          Next run:{' '}
                          {formatDistanceToNow(new Date(task.next_run), { addSuffix: true })}
                        </div>
                      )}
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="primary"
                    onClick={() => runTaskMutation.mutate(task.name)}
                    isLoading={runTaskMutation.isPending}
                  >
                    <Play className="w-4 h-4 mr-2" />
                    Run Now
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
