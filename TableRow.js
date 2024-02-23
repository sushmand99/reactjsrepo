import React from 'react';

const TableRow = ({ row, isSelected, handleRowSelect }) => {
  return (
    <tr>
      <td>{row.name}</td>
      <td>
        <input
          type="checkbox"
          checked={isSelected}
          onChange={() => handleRowSelect(row.id)}
        />
        {row.status}
      </td>
      <td>{row.distribution}</td>
    </tr>
  );
};

export default TableRow;
