import { MainApp } from "./components/mainApp";
import "./App.css";
import { useState } from "react";
import { LoginPage } from "./components/loginPage";

function App() {
  const [loggedIn, setLogIn] = useState<boolean>(false);

  return <div>
    {loggedIn ? <MainApp/>: <LoginPage setLogIn={setLogIn}/>}
  </div>
}

export default App;
