import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from '@/stores/authStore';

// Layout
import SidebarLayout from '@/components/layout/SidebarLayout';

// Pages (these would be created in a full implementation)
import Login from '@/pages/Login';
import Dashboard from '@/pages/Dashboard';
import FeedsList from '@/pages/feeds/FeedsList';
import FeedDetail from '@/pages/feeds/FeedDetail';
import OutboundList from '@/pages/outbound/OutboundList';
import OutboundDetail from '@/pages/outbound/OutboundDetail';
import ProductsList from '@/pages/products/ProductsList';
import ProductDetail from '@/pages/products/ProductDetail';
import BulkUpdate from '@/pages/products/BulkUpdate';
import ManufacturersList from '@/pages/manufacturers/ManufacturersList';
import CategoriesList from '@/pages/categories/CategoriesList';
import AttributesList from '@/pages/attributes/AttributesList';
import LogsList from '@/pages/logs/LogsList';
import Settings from '@/pages/Settings';
import CronMonitor from '@/pages/CronMonitor';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/"
            element={
              <PrivateRoute>
                <SidebarLayout />
              </PrivateRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />

            <Route path="feeds">
              <Route index element={<FeedsList />} />
              <Route path=":id" element={<FeedDetail />} />
            </Route>

            <Route path="outbound">
              <Route index element={<OutboundList />} />
              <Route path=":id" element={<OutboundDetail />} />
            </Route>

            <Route path="products">
              <Route index element={<ProductsList />} />
              <Route path=":id" element={<ProductDetail />} />
              <Route path="bulk-update" element={<BulkUpdate />} />
            </Route>

            <Route path="manufacturers" element={<ManufacturersList />} />
            <Route path="categories" element={<CategoriesList />} />
            <Route path="attributes" element={<AttributesList />} />
            <Route path="logs" element={<LogsList />} />
            <Route path="settings" element={<Settings />} />
            <Route path="cron" element={<CronMonitor />} />
          </Route>
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </QueryClientProvider>
  );
}

export default App;
