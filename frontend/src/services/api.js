import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const fetchMetrics = async () => {
  const response = await axios.get(`${API_URL}/metrics/`);
  return response.data;
};

export const fetchRankings = async (metricName) => {
  const response = await axios.get(`${API_URL}/rankings/${metricName}/`);
  return response.data;
};
