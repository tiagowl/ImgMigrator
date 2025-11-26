import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/Layout';
import { Dashboard } from '@/pages/Dashboard';
import { History } from '@/pages/History';
import { Settings } from '@/pages/Settings';
import { MigrationDetail } from '@/pages/MigrationDetail';
import '@/styles/index.css';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/history" element={<History />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/migrations/:id" element={<MigrationDetail />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;






