import {
  Button,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";
import { getColor, getColorCodeLighter } from "./mainApp";

export const LoginPage = ({
  setLogIn,
  setRole,
}: {
  setLogIn: (newBool: boolean) => void;
  setRole: (newRole: string) => void;
}) => {
  const [username, setUsername] = useState<string>("");

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(event.target.value);
    setRole(event.target.value)
  };

  const sendName = async () => {
    await fetch("http://localhost:8000/login/" + username, {
      mode: "cors",
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setLogIn(true);
        setRole(data.role);
      });
  };

  return (
    <div className="login-container">
      <div
        className="login"
        style={{ background: getColorCodeLighter(username) }}
      >
        <div className="login-title">
          Log in as a {username === "" ? "..." : username}
        </div>
        <div className="login-field">
          <FormControl>
            <RadioGroup row value={username} onChange={handleChange}>
              <FormControlLabel
                value="viewer"
                control={<Radio />}
                label="Viewer"
              />
              <FormControlLabel
                value="creator"
                control={<Radio color="secondary" />}
                label="Creator"
              />
              <FormControlLabel
                value="admin"
                control={<Radio color="success" />}
                label="Admin"
              />
            </RadioGroup>
          </FormControl>
          <Button
            onClick={sendName}
            variant="outlined"
            disabled={username === ""}
            color={getColor(username)}
          >
            <SendIcon />
          </Button>
        </div>
        <div className="desc-title">
          can{" "}
          {username === "admin"
            ? "delete, create, and view"
            : username === "creator"
            ? "create and view"
            : username === "viewer"
            ? "only view"
            : "..."}
        </div>
      </div>
    </div>
  );
};
