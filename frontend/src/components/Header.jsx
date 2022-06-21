import React, { useContext } from "react";
import './header.scss'
import { UserContext } from "../context/UserContext";
import BugReportIcon from '@mui/icons-material/BugReport';
const Header = () => {
  const [token, setToken] = useContext(UserContext);
  const handleLogout = () => {
    setToken(null);
  };

  return (
    <div className="has-text-centered m-6 container">
      <h1 className="title">Issue Tracker</h1>
      <BugReportIcon className="icon" />
      {token && (
        <button className="button" onClick={handleLogout}>
          Logout
        </button>
      )}
    </div>
  );
};

export default Header;