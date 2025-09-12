import React, { useEffect, useRef } from "react";

const InsightBotDashboard = () => {
  const vizRef = useRef(null);

  useEffect(() => {
    // Cleanup previous viz (agar React reload ho)
    return () => {
      if (vizRef.current) {
        vizRef.current.innerHTML = "";
      }
    };
  }, []);

  return (
    <div
      ref={vizRef}
      style={{ width: "100%", height: "100vh", display: "flex", justifyContent: "center" }}
    >
      <iframe
        title="InsightBot Dashboard"
        src="https://public.tableau.com/views/InsightDashboardPublic/InsightBotDashboard?%3AshowVizHome=no&%3Aembed=true#1"
        width="100%"
        height="100%"
        frameBorder="0"
        allowFullScreen
        style={{ minHeight: "1000px" }}
      ></iframe>
    </div>
  );
};

export default InsightBotDashboard;
