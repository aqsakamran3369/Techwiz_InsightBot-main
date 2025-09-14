import React from "react";

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-400 border-t border-gray-800 mt-12">
      <div className="max-w-7xl mx-auto px-6 py-6 text-center">
        <p className="text-sm">
          © {new Date().getFullYear()} <span className="text-white">InsightBot</span>.  
          All rights reserved.
        </p>
        <p className="mt-2 text-xs text-gray-500">
          InsightBot is a project that provides AI-powered insights from news
          articles and dashboards.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
