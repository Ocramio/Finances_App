import { useState } from 'react';
import axios from 'axios';
import qs from 'qs';
import { useNavigate } from 'react-router-dom';

function CadastroForm() {

   const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const handleChange = (e) => {
  const { name, value } = e.target;
  setFormData({
    ...formData,
    [name]: value
  });
};

  const handleSubmit = async (event) => {
    event.preventDefault();
    const body = qs.stringify(formData);
    const headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        withCredentials: true
    };
    
    try {
      const resposta = await axios.post('http://127.0.0.1:8000/auth/token', body, headers);
      if(resposta.status === 200){
        navigate("/dashboard")
      }else{
        alert("Email or password incorrect")
      }
    } catch (error) {
      console.error('API error: ', error);
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <label>Email</label><br></br>
        <input 
          name="username" 
          placeholder="your_email@email.com"
          value={formData.username} 
          onChange={handleChange} 
        /><br></br>
        <label>Password</label><br></br>
        <input 
          name="password" 
          value={formData.password} 
          onChange={handleChange} 
          type='password'
        /><br></br>
        
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default CadastroForm;