import { useEffect, useState } from "react";
import "./App.css";
import api from "./api";

function handleLoginClick() {
  window.location.href = "http://localhost:8000/login";
}


function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get("/users/me");
        setUserData(response.data);
        setLoggedIn(true);
      } catch (error) {
        console.error("Error fetching user data:", error);
        setLoggedIn(false);
      }
    };
    fetchUserData();
  }, []);

  return (
    <>
      {loggedIn ? (
        <div>
          <h1>Welcome, {userData.display_name}!</h1>
          <p>Email: {userData.email}</p>
          <p>Country: {userData.country}</p>
          <p>Product: {userData.product}</p>
          {userData.images && userData.images.length > 0 && (
            <img
              src={userData.images[0].url}
              alt={`${userData.display_name}"s profile`}
              width={userData.images[0].width}
              height={userData.images[0].height}
            />
          )}
        </div>
      ) : (
        <div>
          <h1>Not logged in</h1>
          <button onClick={handleLoginClick}>Login with Spotify</button>
        </div>
      )}
      <button onClick={handleLoginClick}>Login with Spotify</button>
    </>
  );
}

export default App;
