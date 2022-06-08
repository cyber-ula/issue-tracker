import React, { useContext, useEffect, useState } from "react";
import moment from "moment";

import ErrorMessage from "./ErrorMessage";
import LeadModal from "./LeadModal";
import { UserContext } from "../context/UserContext";

const Table = () => {
  const [token] = useContext(UserContext);
  const [leads, setLeads] = useState(null);
  const [bugs, setBugs] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [activeModal, setActiveModal] = useState(false);
  const [id, setId] = useState(null);

  const handleUpdate = async (id) => {
    setId(id);
    setActiveModal(true);
  };


 


  const handleDelete = async (id) => {
    const requestOptions = {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(`https://u-issue-tracker.herokuapp.com/projects/${id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Failed to delete lead");
    }

    getLeads();
  };

  const getLeads = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("https://u-issue-tracker.herokuapp.com/projects", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the leads");
    } else {
      const data = await response.json();
      console.log(data)
      setLeads(data);
      setLoaded(true);
    }
  };

  useEffect(() => {
    getLeads();
  }, []);
  const getBugs = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("https://u-issue-tracker.herokuapp.com/bugs/count", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the leads");
    } else {
      const data = await response.json();
      console.log(data)
      setBugs(data);
      setLoaded(true);
    }
  };

  useEffect(() => {
    getBugs();
  }, []);
 

  const handleModal = () => {
    setActiveModal(!activeModal);
    getLeads();
    setId(null);
  };

  return (
    <>
      <LeadModal
        active={activeModal}
        handleModal={handleModal}
        token={token}
        id={id}
        setErrorMessage={setErrorMessage}
      />
      <button
        className="button is-fullwidth mb-5 is-primary"
        onClick={() => setActiveModal(true)}
      >
        Create Project
      </button>
      <ErrorMessage message={errorMessage} />
      {loaded && leads ? (
        <>
        <table className="table is-fullwidth">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Members</th>
              <th>Bugs</th>
              <th>Owner Email</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {leads.map((lead) => (
              <tr key={lead.Project.id}>
                <td>{lead.Project.name}</td>
                <td>{lead.Project.description}</td>
                <td>{lead.members === null? 0 : lead.members}</td>
                <td>{bugs.map((bug) => lead.Project.id === bug.Project.id? bug.bugs: null )}</td>
                <td>{lead.Project.owner.email}</td>
                <td>{moment(lead.Project.owner.created_at).format("MMM Do YY")}</td>
                <td>
                  <button
                    className="button mr-2 is-info is-light"
                    onClick={() => handleUpdate(lead.Project.id)}
                  >
                    Update
                  </button>
                 
                  <button
                    className="button mr-2 is-danger is-light"
                    onClick={() => handleDelete(lead.Project.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        </>
      ) : (
        <p>Loading</p>
      )}
    </>
  );
};

export default Table;