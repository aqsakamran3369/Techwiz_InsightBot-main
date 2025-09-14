import React, { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Filter, LayoutDashboard, Menu, X, Newspaper } from "lucide-react";

const Header = ({ setShowFilters, showFilters }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="bg-gray-950/80 backdrop-blur-md text-white shadow-md sticky top-0 z-50 border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <img
            src="/logo1.png"
            alt="Logo"
            className="w-10 h-10 rounded-full shadow-md group-hover:scale-110 transition"
          />
          <span className="text-xl font-bold tracking-wide bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            InsightBot
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8">
          <NavLink
            to="/articles"
            className={({ isActive }) =>
              `flex items-center gap-1 border-b-2 transition ${
                isActive
                  ? "text-blue-400 border-blue-400"
                  : "text-gray-300 border-transparent hover:text-blue-300 hover:border-blue-300"
              }`
            }
          >
            <Newspaper className="w-4 h-4" />
            Articles
          </NavLink>

          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `flex items-center gap-1 border-b-2 transition ${
                isActive
                  ? "text-purple-400 border-purple-400"
                  : "text-gray-300 border-transparent hover:text-purple-300 hover:border-purple-300"
              }`
            }
          >
            <LayoutDashboard className="w-4 h-4" />
            Dashboard
          </NavLink>
        </nav>

        {/* Mobile Toggle */}
        <button
          className="md:hidden text-gray-300 hover:text-white"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="md:hidden bg-gray-900 border-t border-gray-800 px-6 py-4 space-y-4">
          <NavLink
            to="/articles"
            onClick={() => setMobileOpen(false)}
            className={({ isActive }) =>
              `block py-2 border-b ${
                isActive ? "text-blue-400 border-blue-400" : "text-gray-300 border-transparent"
              }`
            }
          >
            Articles
          </NavLink>
          <NavLink
            to="/dashboard"
            onClick={() => setMobileOpen(false)}
            className={({ isActive }) =>
              `block py-2 border-b ${
                isActive ? "text-purple-400 border-purple-400" : "text-gray-300 border-transparent"
              }`
            }
          >
            Dashboard
          </NavLink>
        </div>
      )}
    </header>
  );
};

export default Header;
