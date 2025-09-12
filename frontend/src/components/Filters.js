import React from "react";
import { Globe, Search, Calendar } from "lucide-react";

const Filters = ({ dataset, setDataset, language, setLanguage, search, setSearch }) => {
  return (
    <div className="bg-gray-900 p-6 rounded-2xl shadow-lg flex flex-wrap items-center gap-6 justify-between mb-10 border border-gray-800">
      {/* Dataset */}
      <div className="flex items-center gap-3">
        <Globe className="w-5 h-5 text-blue-400" />
        <select
          value={dataset}
          onChange={(e) => setDataset(e.target.value)}
          className="bg-gray-800 text-gray-200 px-4 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
        >
          <option value="">All</option>
          <option value="training">Training</option>
          <option value="testing">Testing</option>
        </select>
      </div>

      {/* Language */}
      <div className="flex items-center gap-3">
        <Globe className="w-5 h-5 text-green-400" />
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="bg-gray-800 text-gray-200 px-4 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-green-500 focus:outline-none transition"
        >
          <option value="">All</option>
          <option value="EN">English</option>
          <option value="AR">Arabic</option>
          <option value="RU">Russian</option>
          <option value="FR">French</option>
        </select>
      </div>

      {/* Search */}
      <div className="flex items-center gap-2 bg-gray-800 px-4 py-2 rounded-lg border border-gray-700 w-full md:w-72">
        <Search className="w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search..."
          className="bg-transparent flex-1 text-gray-200 placeholder-gray-400 focus:outline-none"
        />
      </div>

      {/* Date (future use) */}
      <div className="flex items-center gap-2 text-gray-500 text-sm cursor-not-allowed">
        <Calendar className="w-5 h-5" />
        <span>Select Date</span>
      </div>
    </div>
  );
};

export default Filters;
