import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className='home-container'>
      <h1>LLM Benchmark Simulation</h1>
      <p>Welcome to the LLM Benchmark Simulation Dashboard!</p>
      <p>
        Here you can run simulations and visualize the performance of various
        LLMs.
      </p>

      <div className='button-group'>
        <Link to='/dashboard' className='button'>
          Dashboard
        </Link>
      </div>
    </div>
  );
};

export default Home;
