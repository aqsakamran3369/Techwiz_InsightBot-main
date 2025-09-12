import React, { useEffect, useState } from "react";
import axios from "axios";
import ReactPaginate from "react-paginate";
import { useNavigate } from "react-router-dom";
import InsightBotDashboard from "./InsightBotDashboard";

const ArticleList = ({ dataset, language, search, onSelectArticle }) => {
  const [articles, setArticles] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const limit = 5;
  const navigate = useNavigate();

  const fetchArticles = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/articles/", {
        params: { dataset, language, page, limit, search },
      });

      const { articles: fetchedArticles, total } = res.data;
      setArticles(fetchedArticles || []);
      setTotalPages(Math.ceil((total || 0) / limit) || 1);
    } catch (err) {
      console.error("❌ Error fetching articles:", err);
    }
  };

  useEffect(() => {
    setPage(1); // reset page to 1 on new filter/search
  }, [dataset, language, search]);

  useEffect(() => {
    fetchArticles();
  }, [dataset, language, page, search]);

  return (
    <div>
      <InsightBotDashboard></InsightBotDashboard>
      {articles.map((a, idx) => (
        <div
          key={idx}
          style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px" }}
        >
          <h3>{a.title || a.headline || "Untitled"}</h3>
          <p>{(a.body || "").slice(0, 150)}...</p>
          <button
            onClick={() => {
              onSelectArticle(a);
              navigate("/article");
            }}
          >
            Read More
          </button>
        </div>
      ))}

      <ReactPaginate
        pageCount={totalPages}
        pageRangeDisplayed={2}
        marginPagesDisplayed={1}
        onPageChange={(data) => setPage(data.selected + 1)}
        containerClassName="pagination"
        activeClassName="active"
      />
    </div>
  );
};

export default ArticleList;
