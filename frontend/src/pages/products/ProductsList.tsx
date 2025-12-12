import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { productsApi } from '@/services';
import { FilterParams, Product } from '@/types';
import PageContainer from '@/components/layout/PageContainer';
import DataTable, { Column } from '@/components/shared/DataTable';
import Pagination from '@/components/shared/Pagination';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import ErrorBanner from '@/components/shared/ErrorBanner';
import EmptyState from '@/components/shared/EmptyState';
import Button from '@/components/shared/Button';
import { Plus } from 'lucide-react';

export default function ProductsList() {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<FilterParams>({
    page: 1,
    page_size: 20,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['products', filters],
    queryFn: () => productsApi.list(filters),
  });

  const columns: Column<Product>[] = [
    {
      key: 'sku',
      header: 'SKU',
      render: (row) => (
        <span className="font-medium text-gray-900">{row.sku}</span>
      ),
    },
    {
      key: 'name',
      header: 'Name',
      render: (row) => (
        <span className="text-sm text-gray-600">{row.name}</span>
      ),
    },
    {
      key: 'price',
      header: 'Price',
      render: (row) => (
        <span className="text-sm font-medium">${row.price}</span>
      ),
    },
    {
      key: 'qty',
      header: 'Stock',
      render: (row) => (
        <span className={`text-sm font-medium ${row.qty < 10 ? 'text-red-600' : 'text-gray-900'}`}>
          {row.qty}
        </span>
      ),
    },
    {
      key: 'entity_code',
      header: 'Entity',
      render: (row) => (
        <span className="text-xs px-2 py-1 bg-gray-100 rounded">{row.entity_code}</span>
      ),
    },
  ];

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <PageContainer
      title="Products"
      subtitle="Manage your product catalog"
      action={
        <Button onClick={() => navigate('/products/bulk-update')} variant="primary">
          <Plus className="w-4 h-4 mr-2" />
          Bulk Update
        </Button>
      }
    >
      <div className="space-y-4">
        {/* Filters */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <input
              type="text"
              placeholder="Search by SKU or name..."
              className="px-3 py-2 border border-gray-300 rounded-md"
              onChange={(e) =>
                setFilters({ ...filters, search: e.target.value, page: 1 })
              }
            />
            <input
              type="number"
              placeholder="Min price"
              className="px-3 py-2 border border-gray-300 rounded-md"
              onChange={(e) =>
                setFilters({ ...filters, min_price: e.target.value, page: 1 })
              }
            />
            <input
              type="number"
              placeholder="Max price"
              className="px-3 py-2 border border-gray-300 rounded-md"
              onChange={(e) =>
                setFilters({ ...filters, max_price: e.target.value, page: 1 })
              }
            />
          </div>
        </div>

        {/* Table */}
        {!data?.items.length ? (
          <EmptyState title="No products found" description="No products match your filters" />
        ) : (
          <>
            <DataTable
              data={data.items}
              columns={columns}
              onRowClick={(row) => navigate(`/products/${row.id}`)}
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
