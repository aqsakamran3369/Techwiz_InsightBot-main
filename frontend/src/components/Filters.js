import React from "react";
import { Globe, Search, Database } from "lucide-react";

const Filters = ({ dataset, setDataset, language, setLanguage, search, setSearch }) => {
  return (
    <div className="bg-gray-950/70 backdrop-blur-md p-6 rounded-2xl shadow-xl flex flex-wrap items-center gap-6 justify-between mb-10 border border-gray-800">
      {/* Dataset */}
      <div className="flex items-center gap-3 w-full sm:w-auto">
        <Database className="w-5 h-5 text-indigo-400" />
        <select
          value={dataset}
          onChange={(e) => setDataset(e.target.value)}
          className="bg-gray-900/80 text-gray-200 px-4 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition w-full sm:w-40"
        >
          <option value="">All Datasets</option>
          <option value="training">Training</option>
          <option value="testing">Testing</option>
        </select>
      </div>

      {/* Language */}
      <div className="flex items-center gap-3 w-full sm:w-auto">
        <Globe className="w-5 h-5 text-green-400" />
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="bg-gray-900/80 text-gray-200 px-4 py-2 rounded-lg border border-gray-700 focus:ring-2 focus:ring-green-500 focus:outline-none transition w-full sm:w-40"
        >
          <option value="">All Languages</option>
          <option value="EN">English</option>
          <option value="AR">Arabic</option>
          <option value="RU">Russian</option>
          <option value="FR">French</option>
        </select>
      </div>

      {/* Search */}
      <div className="flex items-center gap-3 bg-gray-900/80 px-4 py-2 rounded-lg border border-gray-700 w-full sm:w-72 hover:border-blue-500 transition">
        <Search className="w-5 h-5 text-blue-400" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search articles..."
          className="bg-transparent flex-1 text-gray-200 placeholder-gray-400 focus:outline-none"
        />
      </div>
    </div>
  );
};

export default Filters;
