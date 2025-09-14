import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ReactPaginate from "react-paginate";

const categoryColors = {
  politics: "bg-red-500",
  sports: "bg-green-500",
  tech: "bg-blue-500",
  business: "bg-yellow-400",
  default: "bg-purple-500",
};

const ArticleList = ({ dataset, language, search, onSelectArticle }) => {
  const [articles, setArticles] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const limit = 9;
  const navigate = useNavigate();

  const fetchArticles = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `http://localhost:5000/api/articles?page=${page}&limit=${limit}&dataset=${dataset}&language=${language}&search=${search || ""}`
      );
      const data = await res.json();

      if (Array.isArray(data.articles)) {
        setArticles(data.articles);
        setTotalPages(Math.ceil((data.total || 0) / limit) || 1);
      } else {
        setArticles([]);
      }
    } catch (err) {
      console.error("❌ Error fetching articles:", err);
      setArticles([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    setPage(1);
  }, [dataset, language, search]);

  useEffect(() => {
    fetchArticles();
  }, [page, dataset, language, search]);

  return (
    <div className="bg-gray-950 min-h-screen p-8 max-w-7xl mx-auto text-gray-100">
      {loading && (
        <p className="text-center text-gray-400 text-lg font-medium animate-pulse">
          Loading articles...
        </p>
      )}
      {!loading && articles.length === 0 && (
        <p className="text-center text-red-400 font-semibold text-lg">
          No articles found.
        </p>
      )}

      {/* GRID OF ARTICLES */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-10">
        {articles.map((a, idx) => {
          const category = (a.dataset_type || "default").toLowerCase();
          const badgeColor = categoryColors[category] || categoryColors.default;
          const imageUrl = `https://picsum.photos/400/250?random=${idx + 100}`;

          return (
            <div
              key={idx}
              className="bg-gray-900/70 backdrop-blur-md border border-gray-700 rounded-2xl shadow-xl overflow-hidden transform hover:scale-[1.04] hover:shadow-2xl transition-all duration-300"
            >
              {/* Image */}
              <img
                src={imageUrl}
                alt="article"
                className="w-full h-56 object-cover"
              />

              {/* Content */}
              <div className="p-6 flex flex-col justify-between h-[250px]">
                <div>
                  <span
                    className={`px-3 py-1 text-xs font-semibold text-white rounded-full ${badgeColor}`}
                  >
                    {a.dataset_type || "News"}
                  </span>
                  <h3
                    className="text-xl font-bold mt-3 mb-3 hover:text-indigo-400 cursor-pointer line-clamp-2"
                    onClick={() => {
                      onSelectArticle({ ...a, image_url: imageUrl });
                      navigate("/article");
                    }}
                  >
                    {a.title || "Untitled"}
                  </h3>
                  <p className="text-gray-400 text-sm mb-5 line-clamp-3">
                    {(a.body || "").slice(0, 120)}...
                  </p>
                </div>

                <button
                  onClick={() => {
                    onSelectArticle({ ...a, image_url: imageUrl });
                    navigate("/article");
                  }}
                  className="px-5 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-sm font-semibold rounded-full hover:from-purple-600 hover:to-indigo-600 transition-all"
                >
                  Read More →
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* PAGINATION */}
      <div className="flex justify-center mt-14">
        <ReactPaginate
          pageCount={totalPages}
          pageRangeDisplayed={2}
          marginPagesDisplayed={1}
          onPageChange={(data) => setPage(data.selected + 1)}
          containerClassName="flex space-x-3"
          pageClassName="px-4 py-2 rounded-full bg-gray-800 text-gray-300 font-medium hover:bg-indigo-600 hover:text-white transition cursor-pointer"
          activeClassName="bg-indigo-500 text-white font-bold shadow-lg cursor-pointer"
          previousLabel="←"
          nextLabel="→"
          previousClassName="px-4 py-2 rounded-full bg-gray-700 text-gray-300 hover:bg-gray-600 transition cursor-pointer"
          nextClassName="px-4 py-2 rounded-full bg-gray-700 text-gray-300 hover:bg-gray-600 transition cursor-pointer"
          disabledClassName="opacity-40 cursor-not-allowed"
        />
      </div>
    </div>
  );
};

export default ArticleList;
