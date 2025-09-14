import React from "react";

const ArticleDetail = ({ article }) => {
  if (!article)
    return (
      <div className="flex justify-center items-center h-screen text-gray-400 text-lg">
        Article not found
      </div>
    );

  return (
    <div className="bg-gray-950 min-h-screen flex flex-col items-center">
      {/* Banner Image with Overlay */}
      <div className="relative w-full h-72 md:h-96">
        <img
          src={`https://picsum.photos/1200/600?random=${article.id || 50}`}
          alt="article banner"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-gray-950 via-black/40 to-transparent"></div>

        {/* Category Badge */}
        <div className="absolute bottom-5 left-5">
          <span className="px-4 py-1 bg-indigo-600 text-white text-sm font-semibold rounded-full shadow-lg">
            {article.dataset_type || "News"}
          </span>
        </div>
      </div>

      {/* Content Box */}
      <div className="w-full max-w-4xl -mt-16 md:-mt-24 relative z-10">
        <div className="bg-gray-900/80 backdrop-blur-md border border-gray-700 rounded-2xl shadow-2xl p-8 md:p-12">
          {/* Title */}
          <h1 className="text-3xl md:text-4xl font-extrabold text-white mb-6 text-center leading-snug">
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
          <div className="prose prose-invert max-w-none text-gray-300 leading-relaxed text-lg">
            {article.body ||
              "No content available for this article. Please check back later."}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleDetail;
