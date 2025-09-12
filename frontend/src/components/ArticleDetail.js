import React from "react";

const ArticleDetail = ({ article }) => {
  if (!article)
    return (
      <div className="flex justify-center items-center h-screen text-gray-400 text-lg">
        Article not found
      </div>
    );

  return (
    <div className="bg-gray-950 min-h-screen px-4 flex justify-center">
      <div className="w-full max-w-3xl bg-gray-900 rounded-2xl shadow-2xl p-10 mt-16 border border-gray-700">
        {/* Title */}
        <h1 className="text-3xl md:text-4xl font-extrabold text-white mb-6 text-center">
          {article.title || article.headline || "Untitled Article"}
        </h1>

        {/* Meta Info */}
        <div className="flex flex-wrap justify-center gap-6 text-gray-400 text-sm mb-8 border-b border-gray-700 pb-4">
          <p>
            <span className="font-semibold text-gray-300">Source:</span>{" "}
            {article.source || "Unknown"}
          </p>
          <p>
            <span className="font-semibold text-gray-300">Published:</span>{" "}
            {article.publication_date || "N/A"}
          </p>
        </div>

        {/* Body */}
        <div className="prose prose-invert max-w-none text-gray-300 leading-relaxed">
          {article.body ||
            "No content available for this article. Please check back later."}
        </div>
      </div>
    </div>
  );
};

export default ArticleDetail;
