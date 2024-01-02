import React from 'react';
import BankTable from './BankTable'; // Import BankTable component

function Reports() {
  return (
    <div className="container">
      {/* Instead of manually entering the FDIC Certificate Number, 
          we use the BankTable component for selection and report generation */}
      <BankTable />
    </div>
  );
}

export default Reports; // Export the component as 'Reports'
