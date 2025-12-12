import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { outboundApi } from '@/services';
import { FilterParams, OutboundJob } from '@/types';
import PageContainer from '@/components/layout/PageContainer';
import DataTable, { Column } from '@/components/shared/DataTable';
import Pagination from '@/components/shared/Pagination';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import EmptyState from '@/components/shared/EmptyState';
import StatusBadge from '@/components/shared/StatusBadge';
import { format } from 'date-fns';

export default function OutboundList() {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<FilterParams>({
    page: 1,
    page_size: 20,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['outbound', filters],
    queryFn: () => outboundApi.list(filters),
  });

  const columns: Column<OutboundJob>[] = [
    {
      key: 'id',
      header: 'ID',
      width: '80px',
    },
    {
      key: 'sync_id',
      header: 'Sync ID',
      render: (row) => (
        <span className="font-mono text-sm">{row.sync_id}</span>
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
    },
    {
      key: 'success_count',
      header: 'Success',
      render: (row) => (
        <span className="text-green-600 font-medium">{row.success_count}</span>
      ),
    },
    {
      key: 'error_count',
      header: 'Errors',
      render: (row) => (
        <span className="text-red-600 font-medium">{row.error_count}</span>
      ),
    },
    {
      key: 'created_at',
      header: 'Created',
      render: (row) => (
        <span className="text-sm text-gray-500">
          {format(new Date(row.created_at), 'MMM d, HH:mm')}
        </span>
      ),
    },
  ];

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <PageContainer
      title="Outbound Jobs"
      subtitle="Track product synchronization jobs"
    >
      <div className="space-y-4">
        {!data?.items.length ? (
          <EmptyState title="No outbound jobs" description="No jobs have been created yet" />
        ) : (
          <>
            <DataTable
              data={data.items}
              columns={columns}
              onRowClick={(row) => navigate(`/outbound/${row.id}`)}
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
