import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { categoriesApi } from '@/services';
import { FilterParams, Category } from '@/types';
import PageContainer from '@/components/layout/PageContainer';
import DataTable, { Column } from '@/components/shared/DataTable';
import Pagination from '@/components/shared/Pagination';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import EmptyState from '@/components/shared/EmptyState';

export default function CategoriesList() {
  const [filters, setFilters] = useState<FilterParams>({
    page: 1,
    page_size: 50,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['categories', filters],
    queryFn: () => categoriesApi.list(filters),
  });

  const columns: Column<Category>[] = [
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
      key: 'path',
      header: 'Path',
      render: (row) => (
        <span className="text-sm text-gray-600">{row.path || '-'}</span>
      ),
    },
    {
      key: 'level',
      header: 'Level',
      render: (row) => (
        <span className="text-sm">{row.level}</span>
      ),
    },
  ];

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <PageContainer
      title="Categories"
      subtitle="Product categories from feeds"
    >
      <div className="space-y-4">
        {!data?.items.length ? (
          <EmptyState title="No categories" description="No categories found" />
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
