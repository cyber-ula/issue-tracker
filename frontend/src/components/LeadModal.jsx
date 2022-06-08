import React, { useEffect, useState } from "react";

const LeadModal = ({ active, handleModal, token, id, setErrorMessage }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  

  useEffect(() => {
    const getLead = async () => {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`https://u-issue-tracker.herokuapp.com/projects/${id}`, requestOptions);

      if (!response.ok) {
        setErrorMessage("Could not get the lead");
      } else {
        const data = await response.json();
        setName(data.first_name);
        setDescription(data.last_name);
        
      }
    };

    if (id) {
      getLead();
    }
  }, [id, token]);

  const cleanFormData = () => {
    setName("");
    setDescription("");
  
  };

  const handleCreateLead = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        name: name,
        description: description,
        
      }),
    };
    const response = await fetch("https://u-issue-tracker.herokuapp.com/projects", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when creating lead");
    } else {
      cleanFormData();
      handleModal();
    }
  };

  const handleUpdateLead = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        name: name,
        description: description,
       
      }),
    };
    const response = await fetch(`https://u-issue-tracker.herokuapp.com/projects/${id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when updating lead");
    } else {
      cleanFormData();
      handleModal();
    }
  };

  return (
    <div className={`modal ${active && "is-active"}`}>
      <div className="modal-background" onClick={handleModal}></div>
      <div className="modal-card">
        <header className="modal-card-head has-background-primary-light">
          <h1 className="modal-card-title">
            {id ? "Update Project" : "Create Project"}
          </h1>
        </header>
        <section className="modal-card-body">
          <form>
            <div className="field">
              <label className="label">Name</label>
              <div className="control">
                <input
                  type="text"
                  placeholder="Enter first name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="input"
                  required
                />
              </div>
            </div>
            <div className="field">
              <label className="label">Description</label>
              <div className="control">
                <input
                  type="text"
                  placeholder="Enter last name"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="input"
                  required
                />
              </div>
            </div>
           
           
            
          </form>
        </section>
        <footer className="modal-card-foot has-background-primary-light">
          {id ? (
            <button className="button is-info" onClick={handleUpdateLead}>
              Update
            </button>
          ) : (
            <button className="button is-primary" onClick={handleCreateLead}>
              Create
            </button>
          )}
          <button className="button" onClick={handleModal}>
            Cancel
          </button>
        </footer>
      </div>
    </div>
  );
};

export default LeadModal;