import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { logsApi } from '@/services';
import { FilterParams, SystemLog } from '@/types';
import PageContainer from '@/components/layout/PageContainer';
import DataTable, { Column } from '@/components/shared/DataTable';
import Pagination from '@/components/shared/Pagination';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import EmptyState from '@/components/shared/EmptyState';
import { format } from 'date-fns';

export default function LogsList() {
  const [filters, setFilters] = useState<FilterParams>({
    page: 1,
    page_size: 50,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['logs', filters],
    queryFn: () => logsApi.list(filters),
  });

  const columns: Column<SystemLog>[] = [
    {
      key: 'id',
      header: 'ID',
      width: '80px',
    },
    {
      key: 'log_type',
      header: 'Type',
      render: (row) => (
        <span className="text-xs px-2 py-1 bg-gray-100 rounded uppercase">
          {row.log_type}
        </span>
      ),
    },
    {
      key: 'log_level',
      header: 'Level',
      render: (row) => {
        const colors = {
          error: 'bg-red-100 text-red-800',
          warning: 'bg-yellow-100 text-yellow-800',
          info: 'bg-blue-100 text-blue-800',
          debug: 'bg-gray-100 text-gray-800',
          critical: 'bg-red-200 text-red-900',
        };
        return (
          <span className={`text-xs px-2 py-1 rounded uppercase ${colors[row.log_level as keyof typeof colors] || colors.debug}`}>
            {row.log_level}
          </span>
        );
      },
    },
    {
      key: 'message',
      header: 'Message',
      render: (row) => (
        <span className="text-sm text-gray-700 line-clamp-1">{row.message}</span>
      ),
    },
    {
      key: 'created_at',
      header: 'Time',
      render: (row) => (
        <span className="text-sm text-gray-500">
          {format(new Date(row.created_at), 'MMM d, HH:mm:ss')}
        </span>
      ),
    },
  ];

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <PageContainer title="System Logs" subtitle="View system activity logs">
      <div className="space-y-4">
        {/* Filters */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              type="text"
              placeholder="Search logs..."
              className="px-3 py-2 border border-gray-300 rounded-md"
              onChange={(e) =>
                setFilters({ ...filters, keyword: e.target.value, page: 1 })
              }
            />
            <select
              className="px-3 py-2 border border-gray-300 rounded-md"
              onChange={(e) =>
                setFilters({ ...filters, log_type: e.target.value, page: 1 })
              }
            >
              <option value="">All Types</option>
              <option value="import">Import</option>
              <option value="export">Export</option>
              <option value="cron">Cron</option>
              <option value="auth">Auth</option>
              <option value="api">API</option>
              <option value="system">System</option>
            </select>
            <select
              className="px-3 py-2 border border-gray-300 rounded-md"
              onChange={(e) =>
                setFilters({ ...filters, log_level: e.target.value, page: 1 })
              }
            >
              <option value="">All Levels</option>
              <option value="error">Error</option>
              <option value="warning">Warning</option>
              <option value="info">Info</option>
              <option value="debug">Debug</option>
            </select>
          </div>
        </div>

        {!data?.items.length ? (
          <EmptyState title="No logs" description="No logs found" />
        ) : (
          <>
            <DataTable data={data.items} columns={columns} />
            <Pagination
              {...data}
              onChange={(page) => setFilters({ ...filters, page })}
            />
          </>
        )}
      </div>
    </PageContainer>
  );
}
