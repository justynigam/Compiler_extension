import { NavLink } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Dashboard', icon: '◉' },
  { to: '/datasets', label: 'Datasets', icon: '◫' },
  { to: '/models', label: 'Models', icon: '⟐' },
  { to: '/predictions', label: 'Predictions', icon: '◈' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-dark-900 border-r border-dark-800 flex flex-col">
      <div className="p-6 border-b border-dark-800">
        <h1 className="text-xl font-bold text-primary-500">ML Platform</h1>
        <p className="text-xs text-gray-500 mt-1">v1.0.0</p>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-600/20 text-primary-500'
                  : 'text-gray-400 hover:bg-dark-800 hover:text-white'
              }`
            }
          >
            <span className="text-lg">{item.icon}</span>
            <span className="text-sm font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-dark-800">
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <div className="w-2 h-2 rounded-full bg-green-500" />
          System Online
        </div>
      </div>
    </aside>
  );
}