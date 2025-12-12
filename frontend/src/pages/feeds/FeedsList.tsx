import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { feedsApi } from '@/services';
import { FilterParams } from '@/types';
import PageContainer from '@/components/layout/PageContainer';
import DataTable, { Column } from '@/components/shared/DataTable';
import Pagination from '@/components/shared/Pagination';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import EmptyState from '@/components/shared/EmptyState';
import StatusBadge from '@/components/shared/StatusBadge';
import { format } from 'date-fns';
import { InboundFeed } from '@/types';

export default function FeedsList() {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<FilterParams>({
    page: 1,
    page_size: 20,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['feeds', filters],
    queryFn: () => feedsApi.list(filters),
  });

  const columns: Column<InboundFeed>[] = [
    {
      key: 'id',
      header: 'ID',
      width: '80px',
    },
    {
      key: 'entity_code',
      header: 'Entity',
      render: (row) => (
        <span className="font-medium text-gray-900">{row.entity_code}</span>
      ),
    },
    {
      key: 'file_name',
      header: 'File Name',
      render: (row) => (
        <span className="text-sm text-gray-600">{row.file_name}</span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (row) => <StatusBadge status={row.status} />,
    },
    {
      key: 'total_count',
      header: 'Total',
      render: (row) => (
        <span className="text-sm">{row.total_count.toLocaleString()}</span>
      ),
    },
    {
      key: 'success_count',
      header: 'Success',
      render: (row) => (
        <span className="text-sm text-green-600 font-medium">
          {row.success_count.toLocaleString()}
        </span>
      ),
    },
    {
      key: 'error_count',
      header: 'Errors',
      render: (row) => (
        <span className="text-sm text-red-600 font-medium">
          {row.error_count.toLocaleString()}
        </span>
      ),
    },
    {
      key: 'updated_at',
      header: 'Updated',
      render: (row) => (
        <span className="text-sm text-gray-500">
          {format(new Date(row.updated_at), 'MMM d, yyyy HH:mm')}
        </span>
      ),
    },
  ];

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <PageContainer title="Inbound Feeds" subtitle="Manage imported product feeds">
      <div className="space-y-4">
        {/* Filters */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <input
              type="text"
              placeholder="Search..."
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              onChange={(e) =>
                setFilters({ ...filters, search: e.target.value, page: 1 })
              }
            />
            <select
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              onChange={(e) =>
                setFilters({ ...filters, status: e.target.value, page: 1 })
              }
            >
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
              <option value="partial">Partial</option>
            </select>
          </div>
        </div>

        {/* Table */}
        {!data?.items.length ? (
          <EmptyState title="No feeds found" description="There are no inbound feeds yet" />
        ) : (
          <>
            <DataTable
              data={data.items}
              columns={columns}
              onRowClick={(row) => navigate(`/feeds/${row.id}`)}
            />
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
