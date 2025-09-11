import React from "react";

const ArticleDetail = ({ article }) => {
  if (!article) return <div>Article not found</div>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>{article.title || article.headline}</h2>
      <p><strong>Source:</strong> {article.source}</p>
      <p><strong>Published:</strong> {article.publication_date}</p>
      <hr />
      <p>{article.body}</p>
    </div>
  );
};

export default ArticleDetail;
