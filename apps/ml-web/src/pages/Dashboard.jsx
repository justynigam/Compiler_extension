import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchDatasets, fetchModels } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState({
    datasets: 0,
    models: 0,
    trainedModels: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const [ds, ms] = await Promise.all([fetchDatasets(), fetchModels()]);
        setStats({
          datasets: ds.total || 0,
          models: ms.total || 0,
          trainedModels:
            ms.models?.filter((m) => m.status === 'trained').length || 0,
        });
      } catch (e) {
        console.error('Failed to load stats', e);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const cards = [
    {
      label: 'Datasets',
      value: stats.datasets,
      link: '/datasets',
      color: 'from-blue-600 to-blue-400',
    },
    {
      label: 'Models',
      value: stats.models,
      link: '/models',
      color: 'from-purple-600 to-purple-400',
    },
    {
      label: 'Trained',
      value: stats.trainedModels,
      link: '/models',
      color: 'from-emerald-600 to-emerald-400',
    },
    {
      label: 'Predictions',
      value: '—',
      link: '/predictions',
      color: 'from-amber-600 to-amber-400',
    },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Dashboard</h2>
      {loading ? (
        <div className="grid grid-cols-4 gap-4">
          {cards.map((_, i) => (
            <div
              key={i}
              className="h-28 bg-dark-800 rounded-xl animate-pulse"
            />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-4 gap-4 mb-8">
          {cards.map((card) => (
            <Link
              key={card.label}
              to={card.link}
              className="bg-dark-800 rounded-xl p-6 hover:bg-dark-800/70 transition-colors border border-dark-800 hover:border-primary-600/30"
            >
              <div
                className={`w-10 h-10 rounded-lg bg-gradient-to-br ${card.color} flex items-center justify-center text-white font-bold mb-3`}
              >
                {card.label[0]}
              </div>
              <div className="text-3xl font-bold">{card.value}</div>
              <div className="text-sm text-gray-400 mt-1">{card.label}</div>
            </Link>
          ))}
        </div>
      )}

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-dark-800 rounded-xl p-6 border border-dark-800">
          <h3 className="font-semibold mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Link
              to="/datasets"
              className="flex items-center gap-3 px-4 py-3 bg-dark-900 rounded-lg text-sm hover:bg-primary-600/10 transition-colors"
            >
              <span className="w-8 h-8 bg-primary-600/20 rounded flex items-center justify-center">
                +
              </span>
              Upload a new dataset
            </Link>
            <Link
              to="/models"
              className="flex items-center gap-3 px-4 py-3 bg-dark-900 rounded-lg text-sm hover:bg-primary-600/10 transition-colors"
            >
              <span className="w-8 h-8 bg-primary-600/20 rounded flex items-center justify-center">
                ±
              </span>
              Create a new model
            </Link>
            <Link
              to="/predictions"
              className="flex items-center gap-3 px-4 py-3 bg-dark-900 rounded-lg text-sm hover:bg-primary-600/10 transition-colors"
            >
              <span className="w-8 h-8 bg-primary-600/20 rounded flex items-center justify-center">
                →
              </span>
              Run predictions
            </Link>
          </div>
        </div>

        <div className="bg-dark-800 rounded-xl p-6 border border-dark-800">
          <h3 className="font-semibold mb-4">Platform Capabilities</h3>
          <ul className="space-y-2 text-sm text-gray-400">
            <li className="flex items-center gap-2">
              <span className="text-green-500">*</span> Dataset upload &amp;
              management
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">*</span> Transformer-based model
              training (PyTorch)
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">*</span> Real-time predictions
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">*</span> SHAP explainability
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">*</span> Network graph analysis
              (NetworkX)
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">*</span> Interactive charts
              (Plotly)
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">*</span> Async task queue (Redis +
              RQ)
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}