import React from 'react';
import './GenerateReportButton.css';

function GenerateReportButton({ onGenerateReport }) {
  return (
    <button className="generate-report-button" onClick={onGenerateReport}>
      Generate Report
    </button>
  );
}

export default GenerateReportButton;
