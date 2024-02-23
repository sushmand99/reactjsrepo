import React, { useState } from 'react';
import Table from './Table';

const App = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRows, setSelectedRows] = useState([]);
  const [selectAll, setSelectAll] = useState(false);

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleRowSelect = (id) => {
    if (selectedRows.includes(id)) {
      setSelectedRows(selectedRows.filter(rowId => rowId !== id));
    } else {
      setSelectedRows([...selectedRows, id]);
    }
  };

  const toggleSelectAll = () => {
    if (selectAll) {
      setSelectedRows([]);
    } else {
      // Assuming filteredData is passed as a prop to Table component
      setSelectedRows(filteredData.map(row => row.id));
    }
    setSelectAll(!selectAll);
  };

  const downloadAsExcel = () => {
    console.log('Downloading selected rows as Excel...');
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => handleSearch(e.target.value)}
      />
      <button onClick={toggleSelectAll}>
        {selectAll ? 'Deselect All' : 'Select All'}
      </button>
      <button onClick={downloadAsExcel}>Download as Excel</button>

      <Table
        searchTerm={searchTerm}
        selectedRows={selectedRows}
        handleRowSelect={handleRowSelect}
      />
    </div>
  );
};

export default App;
