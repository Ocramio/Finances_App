import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "./Signup.css"

function Signup() {

  const navigate = useNavigate();
  const [error, setError] = useState({message: '',color: 'red'});
  const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    confirm_password: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });

    if (name === 'confirm_password') {
      if (value !== formData.password) {
        setError({message:"The passwords don't match", color:"red"});
      }else{
        setError('')
      }
    }else if(name === 'password'){
      if (value !== formData.confirm_password) {
        setError({message:"The passwords don't match", color:"red"});
      }else{
        setError('')
      }
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if(formData.password !== formData.confirm_password){
      return
    }
      
    delete formData.confirm_password
    const body = formData;
    const headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        withCredentials: true
    };
    
    try {
      const response = await axios.post('http://127.0.0.1:8000/auth/signup', body, headers);
      if(response.status === 201){
        setError({message:"Account created", color:"green"})
        wait(5000)
        navigate("/")
      }
    } catch (error) {
      if(error.status === 409){
        setError({message:error.response.data.detail, color:'red'})
      }else{
        setError({message:"Unable to create account, try again later", color:"red"})
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Sign up to Finance App</h1>
        <p>Fill the fields bellow to create an account.</p>
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="email">Email</label><br></br>
            <input 
              id="email"
              name="email" 
              type="email"
              placeholder="your_email@email.com"
              value={formData.email} 
              onChange={handleChange} 
              required
            />
          </div><br></br>
          
          <div className="input-group">
            <label htmlFor="first_name">First Name</label><br></br>
            <input 
              id="first_name"
              name="first_name" 
              value={formData.first_name} 
              onChange={handleChange} 
              required
            />
          </div><br></br>

          <div className="input-group">
            <label htmlFor="last_name">Last Name</label><br></br>
            <input 
              id="last_name"
              name="last_name" 
              value={formData.last_name} 
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

          <div className="input-group">
            <label htmlFor="confirm_password">Confirm Password</label><br></br>
            <input 
              id="confirm_password"
              name="confirm_password" 
              type="password"
              value={formData.confirm_password} 
              onChange={handleChange} 
              required
            />
          </div><br></br>
          <p id='error' style={{color:error.color}}>{error.message}</p>

          <button type="submit" className="login-button">Create Account</button>
        </form><br></br>

        <div className="footer-link">
          Already have an account? <a href="/">Sign in</a>
        </div>
      </div>
    </div>
  );
}

export default Signup;