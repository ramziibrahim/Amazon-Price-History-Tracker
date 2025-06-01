'use client';

import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface PricePoint {
  date: string;
  price: number;
}

interface PriceHistory {
  asin: string;
  history: PricePoint[];
}

interface PriceAlert {
  targetPrice: number;
  email: string;
}

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [priceHistory, setPriceHistory] = useState<PriceHistory | null>(null);
  const [showAlertForm, setShowAlertForm] = useState(false);
  const [alert, setAlert] = useState<PriceAlert>({ targetPrice: 0, email: '' });

  const fetchPriceHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/history', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to fetch price history');
      }

      const data = await response.json();
      setPriceHistory(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const createPriceAlert = async () => {
    if (!priceHistory) return;

    try {
      const response = await fetch('http://localhost:8000/api/alerts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          asin: priceHistory.asin,
          target_price: alert.targetPrice,
          email: alert.email,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create price alert');
      }

      setShowAlertForm(false);
      setAlert({ targetPrice: 0, email: '' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Amazon Price History Tracker</h1>
        
        <div className="mb-8">
          <div className="flex gap-4">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter Amazon product URL"
              className="flex-1 p-2 border rounded"
            />
            <button
              onClick={fetchPriceHistory}
              disabled={loading || !url}
              className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
            >
              {loading ? 'Loading...' : 'Fetch Price History'}
            </button>
          </div>
          
          {error && (
            <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
              {error}
            </div>
          )}
        </div>

        {priceHistory && (
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">
                Price History for ASIN: {priceHistory.asin}
              </h2>
              <button
                onClick={() => setShowAlertForm(true)}
                className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
              >
                Track This Deal
              </button>
            </div>

            {showAlertForm && (
              <div className="mb-6 p-4 bg-gray-50 rounded">
                <h3 className="text-lg font-semibold mb-4">Set Price Alert</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Email</label>
                    <input
                      type="email"
                      value={alert.email}
                      onChange={(e) => setAlert({ ...alert, email: e.target.value })}
                      className="mt-1 block w-full p-2 border rounded"
                      placeholder="Enter your email"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Target Price ($)</label>
                    <input
                      type="number"
                      value={alert.targetPrice}
                      onChange={(e) => setAlert({ ...alert, targetPrice: parseFloat(e.target.value) })}
                      className="mt-1 block w-full p-2 border rounded"
                      placeholder="Enter target price"
                      step="0.01"
                    />
                  </div>
                  <div className="flex gap-4">
                    <button
                      onClick={createPriceAlert}
                      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                      Create Alert
                    </button>
                    <button
                      onClick={() => setShowAlertForm(false)}
                      className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            )}

            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={priceHistory.history}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="date"
                    tickFormatter={(date) => new Date(date).toLocaleDateString()}
                  />
                  <YAxis
                    domain={['auto', 'auto']}
                    tickFormatter={(price) => `$${price}`}
                  />
                  <Tooltip
                    labelFormatter={(date) => new Date(date).toLocaleDateString()}
                    formatter={(price: number) => [`$${price}`, 'Price']}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke="#2563eb"
                    name="Price"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </main>
  );
} 