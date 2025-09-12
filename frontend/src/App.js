import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ArticleList from "./components/ArticlesList";
import ArticleDetail from "./components/ArticleDetail";
import Filters from "./components/Filters";
import InsightBotDashboard from "./components/InsightBotDashboard";

function App() {
  const [dataset, setDataset] = useState("training");
  const [language, setLanguage] = useState("EN");
  const [search, setSearch] = useState(""); // search term
  const [selectedArticle, setSelectedArticle] = useState(null);

  return (
    <Router>
      <div className="bg-gray-900 text-white min-h-screen">
        <Routes>
          {/* Home Page with Articles + Filters */}
          <Route
            path="/"
            element={
              <div className="max-w-4xl mx-auto py-12 px-6">
                <h1 className="text-3xl font-bold mb-6 text-center">
                  InsightBot Articles
                </h1>
                <Filters
                  dataset={dataset}
                  setDataset={setDataset}
                  language={language}
                  setLanguage={setLanguage}
                  search={search}
                  setSearch={setSearch}
                />
                <ArticleList
                  dataset={dataset}
                  language={language}
                  search={search}
                  onSelectArticle={setSelectedArticle}
                />
              </div>
            }
          />

          {/* Article Detail Page */}
          <Route
            path="/article"
            element={<ArticleDetail article={selectedArticle} />}
          />

          {/* Dashboard Page */}
          <Route
            path="/dashboard"
            element={
              <div className="w-full h-screen flex items-center justify-center">
                <InsightBotDashboard />
              </div>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
