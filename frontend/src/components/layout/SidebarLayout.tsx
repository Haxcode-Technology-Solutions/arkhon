import { Outlet } from 'react-router-dom';
import VerticalSideNav from './VerticalSideNav';
import TopBar from './TopBar';

export default function SidebarLayout() {
  return (
    <div className="flex h-screen bg-gray-50">
      <VerticalSideNav />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
