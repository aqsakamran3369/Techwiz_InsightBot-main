import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Filters from "./components/Filters";
import ArticleList from "./components/ArticlesList";
import ArticleDetail from "./components/ArticleDetail";
import InsightBotDashboard from "./components/InsightBotDashboard";
import LandingPage from "./components/LandingPage"; // 👈 new

function Layout() {
  const [dataset, setDataset] = useState("");
  const [language, setLanguage] = useState("");
  const [search, setSearch] = useState("");
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [showFilters, setShowFilters] = useState(true);

  const location = useLocation();

  return (
    <>
      <Header setShowFilters={setShowFilters} showFilters={showFilters} />
      <main className="min-h-screen bg-gray-950">
        <Routes>
          {/* Landing Page */}
          <Route path="/" element={<LandingPage />} />

          {/* Articles Page */}
          <Route
            path="/articles"
            element={
              <>
                {showFilters && (
                  <Filters
                    dataset={dataset}
                    setDataset={setDataset}
                    language={language}
                    setLanguage={setLanguage}
                    search={search}
                    setSearch={setSearch}
                  />
                )}
                <ArticleList
                  dataset={dataset}
                  language={language}
                  search={search}
                  onSelectArticle={setSelectedArticle}
                />
              </>
            }
          />

          <Route path="/article" element={<ArticleDetail article={selectedArticle} />} />
          <Route path="/dashboard" element={<InsightBotDashboard />} />
        </Routes>
      </main>

      {/* Footer sirf dashboard pe hide */}
      {location.pathname !== "/dashboard" && <Footer />}
    </>
  );
}

function App() {
  return (
    <Router>
      <Layout />
    </Router>
  );
}

export default App;
