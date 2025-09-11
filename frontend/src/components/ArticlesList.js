import React, { useEffect, useState } from "react";
import axios from "axios";
import ReactPaginate from "react-paginate";
import { useNavigate } from "react-router-dom";

const ArticleList = ({ dataset, language, onSelectArticle }) => {
  const [articles, setArticles] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const limit = 5;
  const navigate = useNavigate();

  const fetchArticles = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/articles/", {
        params: { dataset, language, page, limit },
      });
      setArticles(res.data.articles || res.data);
      setTotalPages(Math.ceil(res.data.total / limit) || 1);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, [dataset, language, page]);

  return (
    <div>
      {articles.map((a, idx) => (
        <div key={idx} style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px" }}>
          <h3>{a.title || a.headline}</h3>
          <p>{a.body.slice(0, 150)}...</p>
          <button onClick={() => { onSelectArticle(a); navigate("/article"); }}>
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
