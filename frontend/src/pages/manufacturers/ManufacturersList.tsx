import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { manufacturersApi } from '@/services';
import { FilterParams, Manufacturer } from '@/types';
import PageContainer from '@/components/layout/PageContainer';
import DataTable, { Column } from '@/components/shared/DataTable';
import Pagination from '@/components/shared/Pagination';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import EmptyState from '@/components/shared/EmptyState';

export default function ManufacturersList() {
  const [filters, setFilters] = useState<FilterParams>({
    page: 1,
    page_size: 50,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['manufacturers', filters],
    queryFn: () => manufacturersApi.list(filters),
  });

  const columns: Column<Manufacturer>[] = [
    {
      key: 'name',
      header: 'Name',
      render: (row) => (
        <span className="font-medium text-gray-900">{row.name}</span>
      ),
    },
    {
      key: 'code',
      header: 'Code',
      render: (row) => (
        <span className="font-mono text-sm text-gray-600">{row.code || '-'}</span>
      ),
    },
    {
      key: 'website',
      header: 'Website',
      render: (row) =>
        row.website ? (
          <a
            href={row.website}
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-600 hover:underline text-sm"
          >
            {row.website}
          </a>
        ) : (
          <span className="text-gray-400">-</span>
        ),
    },
    {
      key: 'is_system',
      header: 'Type',
      render: (row) => (
        <span className={`text-xs px-2 py-1 rounded ${row.is_system ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}>
          {row.is_system ? 'System' : 'Custom'}
        </span>
      ),
    },
  ];

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <PageContainer
      title="Manufacturers"
      subtitle="Manage product manufacturers"
    >
      <div className="space-y-4">
        {!data?.items.length ? (
          <EmptyState title="No manufacturers" description="No manufacturers found" />
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
