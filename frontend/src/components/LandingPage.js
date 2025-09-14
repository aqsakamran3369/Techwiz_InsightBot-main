import React from "react";
import { Link } from "react-router-dom";
import { Newspaper, LayoutDashboard, Zap, Globe } from "lucide-react";

const LandingPage = () => {
  return (
    <div className="bg-gradient-to-br from-gray-900 via-gray-950 to-black min-h-screen flex flex-col justify-center items-center text-center px-6">
      {/* Hero Section */}
      <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-6">
        Welcome to <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">InsightBot</span>
      </h1>
      <p className="text-lg md:text-xl text-gray-400 max-w-2xl mb-10">
        Your AI-powered companion for exploring curated articles and interactive dashboards.
      </p>

      {/* CTA Buttons */}
      <div className="flex flex-col sm:flex-row gap-6 mb-20">
        <Link
          to="/articles"
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold shadow-lg hover:scale-105 transition transform"
        >
          <Newspaper className="w-5 h-5" />
          Explore Articles
        </Link>
        <Link
          to="/dashboard"
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gray-800 text-gray-200 font-semibold border border-gray-700 hover:bg-gray-700 hover:scale-105 transition transform"
        >
          <LayoutDashboard className="w-5 h-5" />
          Go to Dashboard
        </Link>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-8 max-w-5xl w-full">
        <div className="bg-gray-900/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition">
          <Globe className="w-10 h-10 text-blue-400 mx-auto mb-4" />
          <h3 className="text-white text-lg font-bold mb-2">Multilingual Articles</h3>
          <p className="text-gray-400 text-sm">
            Access curated articles in multiple languages with smart filters.
          </p>
        </div>
        <div className="bg-gray-900/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition">
          <LayoutDashboard className="w-10 h-10 text-purple-400 mx-auto mb-4" />
          <h3 className="text-white text-lg font-bold mb-2">Interactive Dashboard</h3>
          <p className="text-gray-400 text-sm">
            Visualize data and insights in real-time using advanced dashboards.
          </p>
        </div>
        <div className="bg-gray-900/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition">
          <Zap className="w-10 h-10 text-yellow-400 mx-auto mb-4" />
          <h3 className="text-white text-lg font-bold mb-2">Fast & AI-Driven</h3>
          <p className="text-gray-400 text-sm">
            Get instant insights powered by AI for smarter decision making.
          </p>
        </div>
      </div>

      {/* Footer-style Note */}
      <div className="mt-20 text-sm text-gray-500">
        © {new Date().getFullYear()} InsightBot. Built with ❤️ using React & Tailwind.
      </div>
    </div>
  );
};

export default LandingPage;
