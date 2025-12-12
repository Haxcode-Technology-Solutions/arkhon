import { useQuery } from '@tanstack/react-query';
import { settingsApi } from '@/services';
import PageContainer from '@/components/layout/PageContainer';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';

export default function Settings() {
  const { data: settings, isLoading, error } = useQuery({
    queryKey: ['settings'],
    queryFn: () => settingsApi.get(),
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <PageContainer
      title="Settings"
      subtitle="Application configuration"
    >
      <div className="space-y-6">
        {/* Entity Settings */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Entity Settings</h3>
          <div className="space-y-4">
            {Object.entries(settings?.entity_settings || {}).map(([key, value]: [string, any]) => (
              <div key={key} className="border-b border-gray-200 pb-4 last:border-0">
                <h4 className="font-medium text-gray-900 mb-2">{value.name}</h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Code:</span>{' '}
                    <span className="font-mono">{value.entity_code}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Status:</span>{' '}
                    <span className={value.enabled ? 'text-green-600' : 'text-red-600'}>
                      {value.enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* FTP Settings */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">FTP Settings</h3>
          <div className="space-y-4">
            {Object.entries(settings?.ftp_settings || {}).map(([key, value]: [string, any]) => (
              <div key={key} className="border-b border-gray-200 pb-4 last:border-0">
                <h4 className="font-medium text-gray-900 mb-2 capitalize">{key}</h4>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Host:</span> {value.host}
                  </div>
                  <div>
                    <span className="text-gray-600">Port:</span> {value.port}
                  </div>
                  <div>
                    <span className="text-gray-600">Username:</span> {value.username}
                  </div>
                  <div>
                    <span className="text-gray-600">Path:</span> {value.path}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Storage Settings */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Storage Settings</h3>
          <div className="space-y-2 text-sm">
            <div>
              <span className="text-gray-600">Type:</span>{' '}
              <span className="font-medium">{settings?.storage_settings?.type}</span>
            </div>
            <div>
              <span className="text-gray-600">Path:</span>{' '}
              <span className="font-mono">{settings?.storage_settings?.path}</span>
            </div>
          </div>
        </div>

        {/* Sync Settings */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold mb-4">Sync Settings</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Retry Attempts:</span>{' '}
              <span className="font-medium">{settings?.sync_settings?.retry_attempts}</span>
            </div>
            <div>
              <span className="text-gray-600">Retry Delay:</span>{' '}
              <span className="font-medium">{settings?.sync_settings?.retry_delay}s</span>
            </div>
            <div>
              <span className="text-gray-600">Batch Size:</span>{' '}
              <span className="font-medium">{settings?.sync_settings?.batch_size}</span>
            </div>
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
