import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ArticleList from "./components/ArticlesList";
import ArticleDetail from "./components/ArticleDetail";
import Filters from "./components/Filters";

function App() {
  const [dataset, setDataset] = useState("training");
  const [language, setLanguage] = useState("EN");
  const [selectedArticle, setSelectedArticle] = useState(null);

  return (
    <Router>
      <div style={{ width: "800px", margin: "50px auto" }}>
        <h1>InsightBot Articles</h1>
        <Filters
          dataset={dataset}
          setDataset={setDataset}
          language={language}
          setLanguage={setLanguage}
        />
        <Routes>
          <Route
            path="/"
            element={
              <ArticleList
                dataset={dataset}
                language={language}
                onSelectArticle={setSelectedArticle}
              />
            }
          />
          <Route path="/article" element={<ArticleDetail article={selectedArticle} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
