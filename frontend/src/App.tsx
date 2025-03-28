import { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");

  const fetchMessage = async () => {
    try {
      console.log("Backend link:", import.meta.env.VITE_BACKEND_URL + "/api/data");
      const response = await axios.get(import.meta.env.VITE_BACKEND_URL + "/api/data");
      console.log("Before fetching message:", response.data.message);
      setMessage(response.data.message);
      console.log("After fetching message:", response.data.message);
    } catch (error) {
      console.error("Error fetching message:", error);
      setMessage("Error fetching data");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>React + TypeScript + Vite</h1>
      <button onClick={fetchMessage}>Fetch Message</button>
      <p>{message}</p>
    </div>
  );
}

export default App;

