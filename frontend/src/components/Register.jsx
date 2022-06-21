import React, { useContext, useState } from "react";

import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmationPassword, setConfirmationPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);
  const [isRegister, setIsRegister] = useState(false)
  const URL = "https://u-issue-tracker.herokuapp.com"


  const switchMode = () => {
    setIsRegister((prevIsSignup) => !prevIsSignup);}
 
  const submitRegistration = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      //credentials: 'include',
      mode: 'no-cors',
      body: JSON.stringify({ email: email, password: password }),
    };

    const response = await fetch(URL +"/users", requestOptions);
    const data = await response.json();
    console.log(data)
    if (!response.ok) {
      setErrorMessage(data.detail);
      console.log(data.detail)
    } else {
      setToken(data.access_token);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === confirmationPassword && password.length > 5) {
      submitRegistration();
    } else {
      setErrorMessage(
        "Ensure that the passwords match and greater than 5 characters"
      );
    }
  };
  
    const handleLogin = async () => {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
       // credentials: 'include',
       // mode: 'no-cors',
        body: JSON.stringify(
          `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`
        ),
      };
      const response = await fetch( URL +"/login", requestOptions);
      const data = await response.json();
  
      if (!response.ok) {
        setErrorMessage(data.detail);
      } else {
        setToken(data.access_token);
      }
    };

    const handleSubmitLogin = (e) => {
      e.preventDefault();
     handleLogin();
    };

    const submitLoginTest = async () => {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
       // credentials: 'include',
       // mode: 'no-cors',
        body: JSON.stringify(
          `grant_type=&username=${"test@test.com"}&password=${"password123"}&scope=&client_id=&client_secret=`
        ),
      };
  
      const response = await fetch(URL+"/login", requestOptions);
      const data = await response.json();
  
      if (!response.ok) {
        setErrorMessage(data.detail);
      } else {
        setToken(data.access_token);
      }
    };
  
    const handleSubmitTest = (e) => {
      e.preventDefault();
      submitLoginTest();
    };

  return (
    <div className="column">
      <form className="box" onSubmit={!confirmationPassword?handleSubmitLogin: handleSubmit}>
        <h1 className="title has-text-centered">{isRegister? "Register": "Login"}</h1>
       
       <div className="field">
          <label className="label">Email Address</label>
          <div className="control">
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Password</label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        {isRegister && (
        <>
        <div className="field">
          <label className="label">Confirm Password</label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={confirmationPassword}
              onChange={(e) => setConfirmationPassword(e.target.value)}
              className="input"
              required
            />
          </div>
        </div>
        <ErrorMessage message={errorMessage} />
        <br />
        </>
        )}
        <button className="button is-primary" type="submit">
          Submit
        </button>
      </form>
      <div><p>
        {isRegister? "Already have an account?": "Don't have an account?"}
      <span onClick={switchMode}>{isRegister? "Sign In": "Sign Up"}</span> </p></div>
      <button className="button is-primary" onClick={handleSubmitTest}>Login as a test user</button>

    </div>
  );
};

export default Register;