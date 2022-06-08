import React, { useContext } from "react";

import { UserContext } from "../context/UserContext";

const Header = () => {
  const [token, setToken] = useContext(UserContext);
  const [, setEmail] = useContext(UserContext);
  const handleLogout = () => {
    setToken(null);
    setEmail(null);
  };

  return (
    <div className="has-text-centered m-6">
      <h1 className="title">Issue Tracker</h1>
      <p>You are login as:  {localStorage.getItem("email")}</p>
      {token && (
        <button className="button" onClick={handleLogout}>
          Logout
        </button>
      )}
    </div>
  );
};

export default Header;