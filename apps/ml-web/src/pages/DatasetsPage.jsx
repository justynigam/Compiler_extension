import { useEffect, useState, useRef } from 'react';
import { fetchDatasets, uploadDataset } from '../services/api';

export default function DatasetsPage() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef(null);

  const load = async () => {
    try {
      const data = await fetchDatasets();
      setDatasets(data.datasets || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    const form = e.target;
    const file = form.file?.files?.[0];
    if (!file) return;
    setUploading(true);
    const fd = new FormData();
    fd.append('name', form.datasetName.value || file.name);
    fd.append('description', form.description.value || '');
    fd.append('file', file);
    try {
      await uploadDataset(fd);
      form.reset();
      await load();
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Datasets</h2>

      <form
        onSubmit={handleUpload}
        className="bg-dark-800 rounded-xl p-6 mb-6 border border-dark-800 grid grid-cols-4 gap-4"
      >
        <input
          name="datasetName"
          placeholder="Dataset name"
          className="col-span-1 bg-dark-900 border border-dark-800 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-primary-600"
          required
        />
        <input
          name="description"
          placeholder="Description (optional)"
          className="col-span-1 bg-dark-900 border border-dark-800 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-primary-600"
        />
        <input
          type="file"
          accept=".csv"
          className="col-span-1 bg-dark-900 border border-dark-800 rounded-lg px-4 py-2 text-sm file:mr-3 file:px-3 file:py-1 file:rounded file:border-0 file:bg-primary-600 file:text-white file:text-xs"
          required
          ref={fileRef}
        />
        <button
          type="submit"
          disabled={uploading}
          className="col-span-1 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 rounded-lg px-4 py-2 text-sm font-semibold transition-colors"
        >
          {uploading ? 'Uploading...' : 'Upload Dataset'}
        </button>
      </form>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="h-16 bg-dark-800 rounded-xl animate-pulse"
            />
          ))}
        </div>
      ) : datasets.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          No datasets yet. Upload a CSV to get started.
        </div>
      ) : (
        <div className="space-y-2">
          {datasets.map((ds) => (
            <div
              key={ds.id}
              className="bg-dark-800 rounded-xl p-4 flex items-center justify-between border border-dark-800"
            >
              <div>
                <h4 className="font-semibold">{ds.name}</h4>
                <p className="text-xs text-gray-500">
                  {ds.description || 'No description'} — {ds.row_count} rows,{' '}
                  {ds.column_count} columns
                </p>
              </div>
              <div className="text-xs text-gray-500">
                {new Date(ds.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}