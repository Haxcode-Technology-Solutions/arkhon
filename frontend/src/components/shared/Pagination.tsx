import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  onChange: (page: number) => void;
}

export default function Pagination({
  total,
  page,
  page_size,
  total_pages,
  onChange,
}: PaginationProps) {
  const startItem = (page - 1) * page_size + 1;
  const endItem = Math.min(page * page_size, total);

  const pages = [];
  const maxPagesToShow = 7;

  if (total_pages <= maxPagesToShow) {
    for (let i = 1; i <= total_pages; i++) {
      pages.push(i);
    }
  } else {
    if (page <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i);
      pages.push(-1);
      pages.push(total_pages);
    } else if (page >= total_pages - 3) {
      pages.push(1);
      pages.push(-1);
      for (let i = total_pages - 4; i <= total_pages; i++) pages.push(i);
    } else {
      pages.push(1);
      pages.push(-1);
      for (let i = page - 1; i <= page + 1; i++) pages.push(i);
      pages.push(-1);
      pages.push(total_pages);
    }
  }

  return (
    <div className="flex items-center justify-between px-6 py-4 bg-white border-t border-gray-200">
      <div className="text-sm text-gray-700">
        Showing <span className="font-medium">{startItem}</span> to{' '}
        <span className="font-medium">{endItem}</span> of{' '}
        <span className="font-medium">{total}</span> results
      </div>

      <div className="flex items-center space-x-2">
        <button
          onClick={() => onChange(page - 1)}
          disabled={page === 1}
          className="px-3 py-2 rounded-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        {pages.map((pageNum, idx) =>
          pageNum === -1 ? (
            <span key={`ellipsis-${idx}`} className="px-3 py-2 text-gray-500">
              ...
            </span>
          ) : (
            <button
              key={pageNum}
              onClick={() => onChange(pageNum)}
              className={`px-4 py-2 rounded-md border text-sm font-medium transition-colors ${
                page === pageNum
                  ? 'border-primary-600 bg-primary-600 text-white'
                  : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              {pageNum}
            </button>
          )
        )}

        <button
          onClick={() => onChange(page + 1)}
          disabled={page === total_pages}
          className="px-3 py-2 rounded-md border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
