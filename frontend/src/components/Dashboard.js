import React, { useEffect, useState } from 'react';
import { fetchMetrics, fetchRankings } from '../services/api';
import MetricChart from './MetricChart';

const Dashboard = () => {
  const [metrics, setMetrics] = useState([]);
  const [rankings, setRankings] = useState({});

  useEffect(() => {
    const loadMetrics = async () => {
      const data = await fetchMetrics();
      setMetrics(data);
    };

    loadMetrics();
  }, []);

  const handleMetricClick = async (metricName) => {
    const data = await fetchRankings(metricName);
    setRankings((prev) => ({ ...prev, [metricName]: data }));
  };

  return (
    <div>
      <h1>LLM Benchmark Dashboard</h1>
      <div className='metrics-list'>
        {metrics.map((metric) => (
          <div
            key={metric.name}
            onClick={() => {
              handleMetricClick(metric.name);
            }}
            style={{
              cursor: 'pointer',
              padding: '10px',
              margin: '5px 0',
              backgroundColor: '#f0f8ff',
              border: '1px solid #ccc',
              borderRadius: '5px',
              transition: 'background-color 0.3s',
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.backgroundColor = '#e0f0f0')
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.backgroundColor = '#f0f8ff')
            }
          >
            <h2 style={{ margin: '0', fontSize: '1.5rem', color: '#333' }}>
              {metric.name}
            </h2>
          </div>
        ))}
      </div>
      {Object.keys(rankings).map((metricName) => (
        <MetricChart
          key={metricName}
          data={rankings[metricName]}
          metricName={metricName}
        />
      ))}
    </div>
  );
};

export default Dashboard;
