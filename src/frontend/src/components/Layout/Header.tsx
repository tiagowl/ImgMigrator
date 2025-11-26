import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Header: React.FC = () => {
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="bg-white border-b border-neutral-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-md sm:px-lg py-md">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-md">
            <h1 className="text-h4 sm:text-h3 text-primary">Cloud Migrate</h1>
          </Link>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-lg">
            <Link
              to="/"
              className={`text-body font-semibold transition-colors ${
                isActive('/') ? 'text-primary' : 'text-neutral-secondary hover:text-primary'
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/history"
              className={`text-body font-semibold transition-colors ${
                isActive('/history') ? 'text-primary' : 'text-neutral-secondary hover:text-primary'
              }`}
            >
              Histórico
            </Link>
            <Link
              to="/settings"
              className={`text-body font-semibold transition-colors ${
                isActive('/settings') ? 'text-primary' : 'text-neutral-secondary hover:text-primary'
              }`}
            >
              Configurações
            </Link>
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-sm text-neutral-secondary hover:text-primary transition-colors"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {isMenuOpen ? (
                <path d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <nav className="md:hidden mt-md pb-md border-t border-neutral-border pt-md">
            <div className="flex flex-col gap-md">
              <Link
                to="/"
                onClick={() => setIsMenuOpen(false)}
                className={`text-body font-semibold transition-colors py-sm ${
                  isActive('/') ? 'text-primary' : 'text-neutral-secondary hover:text-primary'
                }`}
              >
                Dashboard
              </Link>
              <Link
                to="/history"
                onClick={() => setIsMenuOpen(false)}
                className={`text-body font-semibold transition-colors py-sm ${
                  isActive('/history') ? 'text-primary' : 'text-neutral-secondary hover:text-primary'
                }`}
              >
                Histórico
              </Link>
              <Link
                to="/settings"
                onClick={() => setIsMenuOpen(false)}
                className={`text-body font-semibold transition-colors py-sm ${
                  isActive('/settings') ? 'text-primary' : 'text-neutral-secondary hover:text-primary'
                }`}
              >
                Configurações
              </Link>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
};

