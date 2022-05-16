import { MainApp } from "./components/mainApp";
import "./App.css";
import { useState } from "react";
import { LoginPage } from "./components/loginPage";
import { AppBar, Button, Toolbar, Typography } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import HelpIcon from '@mui/icons-material/Help';
import { getColorCode } from "./components/mainApp";

function App() {
  const [loggedIn, setLogIn] = useState<boolean>(false);
  const [role, setRole] = useState<string>("");

  return (
    <div>
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
