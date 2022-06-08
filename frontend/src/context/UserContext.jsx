import React, { createContext, useEffect, useState } from "react";

export const UserContext = createContext();

export const UserProvider = (props) => {
  const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"));
  const [email, setEmail] = useState(localStorage.getItem("email"))
  useEffect(() => {
    const fetchUser = async () => {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };

      const response = await fetch("/users/me", requestOptions);

      if (!response.ok) {
        setToken(null);
        
      }
      localStorage.setItem("awesomeLeadsToken", token);
      localStorage.setItem("email", email)
      const data = await response.json();

      console.log(data.email)
      setEmail(data.email);

    };
    fetchUser();
  }, [token,email]);

  return (
    <>
    <UserContext.Provider value={[token, setToken]}>
      {props.children}
    </UserContext.Provider>
    
    </>
  );
};