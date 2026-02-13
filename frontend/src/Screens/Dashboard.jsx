import React, { useState, useEffect } from 'react';

const UserTable = () => {
  const [data, setData] = useState([]);

  // Simulando a chamada da API
  useEffect(() => {
    fetch('sua-api.com/users')
      .then(response => response.json())
      .then(json => setData(json));
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Lista de Usuários</h2>
      <table border="1" style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f2f2f2' }}>
            <th>ID</th>
            <th>Nome</th>
            <th>E-mail</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.name}</td>
              <td>{item.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {data.length === 0 && <p>Nenhum dado encontrado.</p>}
    </div>
  );
};

export default UserTable;