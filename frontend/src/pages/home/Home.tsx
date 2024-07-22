import axios from "axios";
import React, { useState } from "react";

interface ResponseType {
  response: string;
}

const Home = () => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [reply, setReply] = useState<string>("");

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
  };

  const handleSearch = async () => {
    try {
      const payload = {
        user_id: 1,
        question: searchQuery,
      };
      await axios
        .post("http://127.0.0.1:8000/generate_response", payload)
        .then((response) => setReply(response.data.response))
        .catch((err) => console.log(err));
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="w-100 h-100 d-flex justify-content-center align-items-center flex-column">
      <div
        className="row w-100 d-flex flex-row m-2 text-left"
        style={{
          height: "9%",
        }}
      >
        <div className="col-1">
          <b>Disclaimer:</b>
        </div>
        <div className="col-11">This is a test application which is a POC.</div>
      </div>
      <div
        className="row w-100 text-center"
        style={{
          height: "80%",
        }}
      >
        {reply}
      </div>
      <div
        className="row w-100 m-2 d-flex justify-content-center align-items-center flex-row"
        style={{
          height: "9%",
        }}
      >
        <input
          type="text"
          className="form-control w-50"
          id="inputText"
          placeholder="Enter Search Query.."
          value={searchQuery}
          onChange={handleChange}
        />
        <button
          type="button"
          className="btn btn-primary"
          onClick={handleSearch}
        >
          Search
        </button>
      </div>
    </div>
  );
};

export default Home;
