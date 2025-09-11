// src/components/Filters.js
import React from "react";

const Filters = ({ dataset, setDataset, language, setLanguage }) => {
  return (
    <div style={{ marginBottom: "20px" }}>
      <label>
        Dataset:
        <select value={dataset} onChange={(e) => setDataset(e.target.value)}>
          <option value="training">Training</option>
          <option value="testing">Testing</option>
        </select>
      </label>
      <label style={{ marginLeft: "20px" }}>
        Language:
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="EN">English</option>
          <option value="AR">Arabic</option>
          <option value="RU">Russian</option>
        </select>
      </label>
    </div>
  );
};

export default Filters;
