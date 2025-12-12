import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { attributesApi } from '@/services';
import { FilterParams, Attribute } from '@/types';
import PageContainer from '@/components/layout/PageContainer';
import DataTable, { Column } from '@/components/shared/DataTable';
import Pagination from '@/components/shared/Pagination';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import EmptyState from '@/components/shared/EmptyState';

export default function AttributesList() {
  const [filters, setFilters] = useState<FilterParams>({
    page: 1,
    page_size: 50,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['attributes', filters],
    queryFn: () => attributesApi.list(filters),
  });

  const columns: Column<Attribute>[] = [
    {
      key: 'label',
      header: 'Label',
      render: (row) => (
        <span className="font-medium text-gray-900">{row.label}</span>
      ),
    },
    {
      key: 'code',
      header: 'Code',
      render: (row) => (
        <span className="font-mono text-sm text-gray-600">{row.code}</span>
      ),
    },
    {
      key: 'attribute_type',
      header: 'Type',
      render: (row) => (
        <span className="text-xs px-2 py-1 bg-gray-100 rounded">{row.attribute_type}</span>
      ),
    },
    {
      key: 'input_type',
      header: 'Input',
      render: (row) => (
        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">{row.input_type}</span>
      ),
    },
    {
      key: 'group_name',
      header: 'Group',
      render: (row) => (
        <span className="text-sm text-gray-600">{row.group_name || '-'}</span>
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
      title="Attributes"
      subtitle="Manage product attributes (EAV)"
    >
      <div className="space-y-4">
        {!data?.items.length ? (
          <EmptyState title="No attributes" description="No attributes found" />
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
