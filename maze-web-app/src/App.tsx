import { MainApp } from "./components/mainApp";
import "./App.css";
import { useState } from "react";
import { LoginPage } from "./components/loginPage";

function App() {
  const [loggedIn, setLogIn] = useState<boolean>(false);
  const [role, setRole] = useState<string>("viewer");

  return <div>
    {loggedIn ? <MainApp role={role}/>: <LoginPage setLogIn={setLogIn} setRole={setRole}/>}
  </div>
}

export default App;
