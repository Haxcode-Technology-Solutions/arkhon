import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@/services';
import PageContainer from '@/components/layout/PageContainer';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import { Package, Download, Upload, AlertCircle, Clock } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export default function Dashboard() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => dashboardApi.getStats(),
  });

  const { data: timeline } = useQuery({
    queryKey: ['dashboard-timeline'],
    queryFn: () => dashboardApi.getTimeline(),
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  const statCards = [
    {
      label: 'Total Products',
      value: stats?.total_products || 0,
      icon: Package,
      color: 'blue',
    },
    {
      label: 'Outbound Jobs',
      value: stats?.total_outbound_jobs || 0,
      icon: Upload,
      color: 'green',
    },
    {
      label: 'Pending Feeds',
      value: stats?.pending_inbound_feeds || 0,
      icon: Download,
      color: 'yellow',
    },
    {
      label: 'Failed Feeds',
      value: stats?.failed_inbound_feeds || 0,
      icon: AlertCircle,
      color: 'red',
    },
  ];

  return (
    <PageContainer
      title="Dashboard"
      subtitle="Overview of your integration platform"
    >
      <div className="space-y-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statCards.map((stat) => (
            <div
              key={stat.label}
              className="bg-white rounded-lg border border-gray-200 p-6"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {stat.value.toLocaleString()}
                  </p>
                </div>
                <div className={`p-3 rounded-lg bg-${stat.color}-100`}>
                  <stat.icon className={`w-6 h-6 text-${stat.color}-600`} />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Activity Stats */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Recent Activity (Last 7 Days)
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Products Added</span>
                <span className="text-lg font-semibold text-gray-900">
                  {stats?.recent_activity?.products_last_7_days || 0}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Feeds Processed</span>
                <span className="text-lg font-semibold text-gray-900">
                  {stats?.recent_activity?.feeds_last_7_days || 0}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Queue Status</span>
                <span className="text-lg font-semibold text-yellow-600">
                  {stats?.queue_status?.pending || 0} pending
                </span>
              </div>
            </div>
          </div>

          {/* Timeline */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Recent Operations
            </h3>
            <div className="space-y-4">
              {timeline?.timeline?.slice(0, 5).map((event: any, idx: number) => (
                <div key={idx} className="flex items-start space-x-3">
                  <div className="mt-1">
                    <Clock className="w-4 h-4 text-gray-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900">
                      {event.type === 'inbound_feed' ? 'Feed Import' : 'Outbound Job'}:{' '}
                      {event.file_name || event.sync_id}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {formatDistanceToNow(new Date(event.timestamp), {
                        addSuffix: true,
                      })}
                    </p>
                  </div>
                  <span
                    className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                      event.status === 'completed'
                        ? 'bg-green-100 text-green-800'
                        : event.status === 'failed'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}
                  >
                    {event.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
