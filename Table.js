import React from 'react';
import TableRow from './TableRow';

const Table = ({ searchTerm, selectedRows, handleRowSelect }) => {
  // Assuming filteredData is passed as a prop
  const filteredData = [];

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Status</th>
          <th>Distribution</th>
        </tr>
      </thead>
      <tbody>
        {filteredData.map(row => (
          <TableRow
            key={row.id}
            row={row}
            isSelected={selectedRows.includes(row.id)}
            handleRowSelect={handleRowSelect}
          />
        ))}
      </tbody>
    </table>
  );
};

export default Table;
