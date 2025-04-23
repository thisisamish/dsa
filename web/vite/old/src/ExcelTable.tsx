const data = [
  {
    id: 1,
    name: "Row 1",
    col2: "Data 1-2",
    col3: "Data 1-3",
    col4: "Data 1-4",
    col5: "Data 1-5",
    col6: "Data 1-6",
    col7: "Data 1-7",
    col8: "Data 1-8",
  },
  {
    id: 2,
    name: "Row 2",
    col2: "Data 2-2",
    col3: "Data 2-3",
    col4: "Data 2-4",
    col5: "Data 2-5",
    col6: "Data 2-6",
    col7: "Data 2-7",
    col8: "Data 2-8",
  },
  // Add more data rows as needed
];

const TableWithFixedColumn = () => {
  return (
    <div className="overflow-x-auto relative">
      {" "}
      {/* Container for horizontal scrolling */}
      <table className="w-full table-auto">
        <thead>
          <tr>
            <th className="sticky left-0 bg-gray-200 text-left px-4 py-2 z-10">
              {" "}
              {/* Sticky header cell */}
              Column Name
            </th>
            <th className="text-left px-4 py-2">Column 2</th>
            <th className="text-left px-4 py-2">Column 3</th>
            <th className="text-left px-4 py-2">Column 4</th>
            <th className="text-left px-4 py-2">Column 5</th>
            <th className="text-left px-4 py-2">Column 6</th>
            <th className="text-left px-4 py-2">Column 7</th>
            <th className="text-left px-4 py-2">Column 8</th>
            {/* Add more header columns as needed */}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id}>
              <td className="sticky left-0 bg-white border-r text-left px-4 py-2 z-10">
                {" "}
                {/* Sticky data cell */}
                {row.name}
              </td>
              <td className="border-r px-4 py-2">{row.col2}</td>
              <td className="border-r px-4 py-2">{row.col3}</td>
              <td className="border-r px-4 py-2">{row.col4}</td>
              <td className="border-r px-4 py-2">{row.col5}</td>
              <td className="border-r px-4 py-2">{row.col6}</td>
              <td className="border-r px-4 py-2">{row.col7}</td>
              <td className="border-r px-4 py-2">{row.col8}</td>
              {/* Add more data cells as needed */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableWithFixedColumn;
