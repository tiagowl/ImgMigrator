import React from 'react';
import { Header } from './Header';
import { Toaster } from 'react-hot-toast';

export interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-neutral-background">
      <Header />
      <main className="max-w-7xl mx-auto px-md sm:px-lg py-lg sm:py-xl">
        {children}
      </main>
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 5000,
          style: {
            background: '#fff',
            color: '#1A1A1A',
            border: '1px solid #CCCCCC',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            fontSize: '14px',
            maxWidth: '90vw',
          },
          success: {
            iconTheme: {
              primary: '#00AA44',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#CC0000',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  );
};


