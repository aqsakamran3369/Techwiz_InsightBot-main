import React from "react";

const Filters = ({ dataset, setDataset, language, setLanguage, search, setSearch }) => {
  return (
    <div style={{ marginBottom: "20px" }}>
      <label>
        Dataset:
        <select value={dataset} onChange={(e) => setDataset(e.target.value)}>
          <option value="">All</option>
          <option value="training">Training</option>
          <option value="testing">Testing</option>
        </select>
      </label>

      <label style={{ marginLeft: "20px" }}>
        Language:
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="">All</option>
          <option value="EN">English</option>
          <option value="AR">Arabic</option>
          <option value="RU">Russian</option>
          <option value="FR">French</option>
        </select>
      </label>

      <label style={{ marginLeft: "20px" }}>
        Search:
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Enter keyword"
          style={{ marginLeft: "5px" }}
        />
      </label>
    </div>
  );
};

export default Filters;
