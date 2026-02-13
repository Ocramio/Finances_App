import { useState } from 'react';
import axios from 'axios';
import qs from 'qs';
import { useNavigate } from 'react-router-dom';
import "./Login.css"

function LoginForm() {

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
    <div className="login-container">
      <div className="login-card">
        <h1>Welcome to Finance App</h1>
        <p>Insert your email and password to login.</p>
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="username">Email</label><br></br>
            <input 
              id="username"
              name="username" 
              type="email"
              placeholder="your_email@email.com"
              value={formData.username} 
              onChange={handleChange} 
              required
            />
          </div><br></br>

          <div className="input-group">
            <label htmlFor="password">Password</label><br></br>
            <input 
              id="password"
              name="password" 
              type="password"
              value={formData.password} 
              onChange={handleChange} 
              required
            />
          </div><br></br>

          <button type="submit" className="login-button">Submit</button>
        </form><br></br>

        <div className="footer-link">
          Don't have an account? <a href="/signup">Sign up</a>
        </div>
      </div>
    </div>
  );
}

export default LoginForm;