import { MainApp } from "./components/mainApp";
import "./App.css";
import { useState } from "react";
import { LoginPage } from "./components/loginPage";
import { AppBar, Button, Toolbar, Typography } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import HelpIcon from "@mui/icons-material/Help";
import CloseIcon from "@mui/icons-material/Close";
import { getColorCode } from "./components/mainApp";

function App() {
  const [loggedIn, setLogIn] = useState<boolean>(false);
  const [helpPopup, setHelpPopup] = useState<boolean>(false);
  const [role, setRole] = useState<string>("");

  return (
    <div>
      {helpPopup && (
        <div className="popup">
          <div className="close">
            <button
              onClick={() => setHelpPopup(!helpPopup)}
              className="close-button"
            >
              <CloseIcon fontSize="small" />
            </button>
            <div style={{ fontSize: "2.5em" }}>About</div>
          </div>
          <div className="popup-desc" style={{ fontSize: "1.2em" }}>
            <li>Maze Generator is a web app that allows for the generation of random mazes.</li>
            <li>An RBAC system is used to give permissions for the user.</li>
            <li>You can always reload the page and use a different role.</li>
          </div>
        </div>
      )}
      <div className="App">
        <AppBar position="static" style={{ background: getColorCode(role) }}>
          <Toolbar>
            <div>
              <form action="https://github.com/NabilNYMansour/Maze-Gen-Web-App">
                <a href="https://github.com/NabilNYMansour/Maze-Gen-Web-App">
                  <button
                    type="submit"
                    className="topnavbutton"
                    style={{ background: getColorCode(role) }}
                  >
                    <GitHubIcon />
                  </button>
                </a>
              </form>
            </div>
            <Typography
              fontFamily="Courier New"
              variant="h6"
              component="div"
              sx={{ flexGrow: 1 }}
            >
              Maze Generator
            </Typography>
            <button
              type="submit"
              className="topnavbutton"
              style={{ background: getColorCode(role) }}
              onClick={() => setHelpPopup(!helpPopup)}
            >
              <HelpIcon />
            </button>
          </Toolbar>
        </AppBar>
        {loggedIn ? (
          <MainApp role={role} />
        ) : (
          <LoginPage setLogIn={setLogIn} setRole={setRole} />
        )}
      </div>
    </div>
  );
}

export default App;
