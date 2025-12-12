import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Download,
  Upload,
  Package,
  Factory,
  FolderTree,
  ListTree,
  FileText,
  Settings,
  Clock,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { name: 'Inbound Feeds', to: '/feeds', icon: Download },
  { name: 'Outbound Jobs', to: '/outbound', icon: Upload },
  { name: 'Products', to: '/products', icon: Package },
  { name: 'Manufacturers', to: '/manufacturers', icon: Factory },
  { name: 'Categories', to: '/categories', icon: FolderTree },
  { name: 'Attributes', to: '/attributes', icon: ListTree },
  { name: 'System Logs', to: '/logs', icon: FileText },
  { name: 'Cron Monitor', to: '/cron', icon: Clock },
  { name: 'Settings', to: '/settings', icon: Settings },
];

export default function VerticalSideNav() {
  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col">
      {/* Logo */}
      <div className="h-16 flex items-center px-6 border-b border-gray-800">
        <h1 className="text-xl font-bold">Arkhon</h1>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`
            }
          >
            <item.icon className="w-5 h-5 mr-3" />
            <span className="text-sm font-medium">{item.name}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-800">
        <p className="text-xs text-gray-500 text-center">
          Arkhon Integration Platform v1.0
        </p>
      </div>
    </div>
  );
}
