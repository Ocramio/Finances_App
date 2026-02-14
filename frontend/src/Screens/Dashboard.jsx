import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


const UserTable = () => {
  const [data, setData] = useState([]);

  const hasAlerted = useRef(false);
  const navigate = useNavigate();

  useEffect(() => {
  const fetchExpenses = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/expenses/list`,{
        withCredentials: true
      });

      setData(Array.isArray(response.data) ? response.data : []);

    } catch (err) {
      if (!hasAlerted.current) {
        const apiErrorMessage = err.response.data.detail;
        console.error("Error", apiErrorMessage);
        
        alert('Login Expired');
        hasAlerted.current = true;
        navigate('/');
      }
    }
  };

  fetchExpenses();
}, [navigate]);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Expenses List</h2>
      <table border="1" style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f2f2f2' }}>
            <th>Expense ID</th>
            <th>Expense type</th>
            <th>Expense Value</th>
            <th>Expense Description</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.expense_id}>
              <td>{item.expense_id}</td>
              <td>{item.expense_type}</td>
              <td>{item.expense_value}</td>
              <td>{item.expense_description}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {data.length === 0 && <p>No data found.</p>}
    </div>
  );
};

export default UserTable;