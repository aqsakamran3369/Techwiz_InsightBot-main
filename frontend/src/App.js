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
      <Routes>
        {/* Home Page with Articles + Filters */}
        <Route
          path="/"
          element={
            <div style={{ maxWidth: "1000px", margin: "50px auto", padding: "0 20px" }}>
              <h1>InsightBot Articles</h1>
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
            <div style={{ width: "100%", height: "100vh", textAlign: "center", marginTop: "0" }}>
              <InsightBotDashboard />
            </div>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
