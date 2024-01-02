import React from 'react';
import './SelectedBank.css';

function SelectedBanks({ selectedBanks, onRemoveBank }) {
  return (
    <div className="selected-banks">
      <h2>Selected Banks</h2>
      <ul>
        {selectedBanks.map((bank) => (
          <li key={bank.CERT} className="selected-bank">
            <span>{bank.NAME}</span>
            <span>{bank.CERT}</span>
            <button onClick={() => onRemoveBank(bank.CERT)} className="remove-button">
              Remove
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SelectedBanks;
