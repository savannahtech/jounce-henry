import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register necessary components
Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const MetricChart = ({ data, metricName }) => {
  const chartData = {
    labels: data.map((item) => item.llm),
    datasets: [
      {
        label: 'Mean Value',
        data: data.map((item) => item.mean_value),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'LLM Mean Values',
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'LLMs',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Mean Value',
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div>
      <h3>{metricName} Chart</h3>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default MetricChart;
