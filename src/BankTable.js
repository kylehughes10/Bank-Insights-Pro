import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import SearchBar from './SearchBar';
import SelectedBanks from './SelectedBanks';
import GenerateReportButton from './GenerateReportButton';

function BankTable() {
  const [banks, setBanks] = useState([]);
  const [filteredBanks, setFilteredBanks] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchColumn, setSearchColumn] = useState('NAME');
  const [selectedBanks, setSelectedBanks] = useState([]);

  // Fetch and set banks data
  useEffect(() => {
    const csvFilePath = '/institutions.csv'; // Make sure to put the CSV in the public folder
    fetch(csvFilePath)
      .then(response => response.text())
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            setBanks(results.data);
          }
        });
      })
      .catch(error => {
        console.error('Error loading CSV file:', error);
      });
  }, []);

  // Filter banks data based on searchTerm and searchColumn
  useEffect(() => {
    const lowerCaseSearchTerm = searchTerm.toLowerCase();
    const filtered = banks.filter(bank =>
      bank[searchColumn]?.toString().toLowerCase().includes(lowerCaseSearchTerm)
    );
    setFilteredBanks(filtered);
  }, [searchTerm, searchColumn]);

  const handleAddBank = (bank) => {
    setSelectedBanks(prevSelectedBanks => [...prevSelectedBanks, bank]);
  };

  const handleRemoveBank = (cert) => {
    setSelectedBanks(prevSelectedBanks =>
      prevSelectedBanks.filter(bank => bank.CERT !== cert)
    );
  };

  const handleGenerateReport = async () => {
    try {
      const certs = selectedBanks.map(bank => bank.CERT);
      const response = await axios.post('http://localhost:5000/run-ubpr', { certs });
      console.log(response.data);
    } catch (error) {
      console.error('Error generating the report:', error);
    }
  };

  return (
    <div>
      <SelectedBanks selectedBanks={selectedBanks} onRemoveBank={handleRemoveBank} />
      <SearchBar setSearchTerm={setSearchTerm} setSearchColumn={setSearchColumn} />
      <GenerateReportButton onGenerateReport={handleGenerateReport} />
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>CERT</th>
            <th>ASSET</th>
            <th>CITY</th>
            <th>STNAME</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {filteredBanks.map((bank) => (
            <tr key={bank.CERT}>
              <td>{bank.NAME}</td>
              <td>{bank.CERT}</td>
              <td>{bank.ASSET}</td>
              <td>{bank.CITY}</td>
              <td>{bank.STNAME}</td>
              <td>
                <button onClick={() => handleAddBank(bank)}>Add</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BankTable;
