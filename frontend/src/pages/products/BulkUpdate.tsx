import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { productsApi } from '@/services';
import PageContainer from '@/components/layout/PageContainer';
import Button from '@/components/shared/Button';
import { ArrowLeft } from 'lucide-react';
import toast from 'react-hot-toast';

export default function BulkUpdate() {
  const navigate = useNavigate();
  const [productIds, setProductIds] = useState('');
  const [targetField, setTargetField] = useState<'price' | 'qty'>('price');
  const [mode, setMode] = useState<'percent' | 'fixed'>('percent');
  const [value, setValue] = useState('');
  const [reason, setReason] = useState('');

  const mutation = useMutation({
    mutationFn: (data: any) => productsApi.bulkUpdate(data),
    onSuccess: (data) => {
      toast.success(`Bulk update job created: ${data.sync_id}`);
      navigate(`/outbound/${data.job_id}`);
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Bulk update failed');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const ids = productIds
      .split(',')
      .map((id) => Number(id.trim()))
      .filter((id) => !isNaN(id));

    if (ids.length === 0) {
      toast.error('Please enter valid product IDs');
      return;
    }

    mutation.mutate({
      product_ids: ids,
      target_field: targetField,
      mode,
      value: Number(value),
      reason,
    });
  };

  return (
    <PageContainer
      title="Bulk Update Products"
      subtitle="Update multiple products at once"
      action={
        <Button onClick={() => navigate('/products')} variant="secondary">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Products
        </Button>
      }
    >
      <div className="bg-white rounded-lg border border-gray-200 p-6 max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Product IDs */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product IDs (comma-separated)
            </label>
            <textarea
              value={productIds}
              onChange={(e) => setProductIds(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              rows={3}
              placeholder="1, 2, 3, 4, 5"
              required
            />
          </div>

          {/* Target Field */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Update Field
            </label>
            <select
              value={targetField}
              onChange={(e) => setTargetField(e.target.value as 'price' | 'qty')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="price">Price</option>
              <option value="qty">Quantity</option>
            </select>
          </div>

          {/* Mode */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Update Mode
            </label>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value as 'percent' | 'fixed')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="percent">Percentage Change</option>
              <option value="fixed">Fixed Amount</option>
            </select>
          </div>

          {/* Value */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Value {mode === 'percent' && '(%)'}
            </label>
            <input
              type="number"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder={mode === 'percent' ? '10' : '5.00'}
              step="0.01"
              required
            />
            <p className="mt-1 text-sm text-gray-500">
              {mode === 'percent'
                ? 'Enter percentage (positive to increase, negative to decrease)'
                : 'Enter fixed amount to add/subtract'}
            </p>
          </div>

          {/* Reason */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Reason (optional)
            </label>
            <input
              type="text"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="End of season sale"
            />
          </div>

          {/* Submit */}
          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate('/products')}
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary" isLoading={mutation.isPending}>
              Create Bulk Update Job
            </Button>
          </div>
        </form>
      </div>
    </PageContainer>
  );
}
