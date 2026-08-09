import Plot from 'react-plotly.js';

export default function PlotlyChart({ data, layout, title, className = '' }) {
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return (
      <div className="flex items-center justify-center h-96 bg-dark-800 rounded-xl text-gray-500">
        No chart data available
      </div>
    );
  }

  const mergedLayout = {
    paper_bgcolor: '#11111b',
    plot_bgcolor: '#11111b',
    font: { color: '#cbd5e1' },
    margin: { t: 40, r: 20, b: 40, l: 60 },
    ...layout,
  };

  return (
    <div className={`bg-dark-800 rounded-xl p-4 ${className}`}>
      {title && (
        <h3 className="text-sm font-semibold text-gray-300 mb-3">{title}</h3>
      )}
      <Plot
        data={data}
        layout={mergedLayout}
        useResizeHandler
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false, responsive: true }}
      />
    </div>
  );
}