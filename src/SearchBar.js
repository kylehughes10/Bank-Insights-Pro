
import React from 'react';
import './SearchBar.css';

function SearchBar({ setSearchTerm, setSearchColumn }) {
  const handleSearchTermChange = (event) => {
    // Update the search term when the input changes
    setSearchTerm(event.target.value);
  };

  const handleSearchColumnChange = (event) => {
    // Update the search column when the dropdown changes
    setSearchColumn(event.target.value);
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search..."
        onChange={handleSearchTermChange}
        className="search-input"
      />
      <select onChange={handleSearchColumnChange} className="search-dropdown">
        <option value="NAME">Name</option>
        <option value="CERT">Cert</option>
        <option value="ASSET">Asset</option>
        <option value="CITY">City</option>
        <option value="STNAME">State</option>
      </select>
    </div>
  );
}

export default SearchBar;
