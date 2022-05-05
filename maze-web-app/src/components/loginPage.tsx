import { Button, TextField } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";

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
      <div className="login">
        <div className="login-title">Log in</div>
        <div className="login-field">
          <TextField
            onKeyDown={(e: React.KeyboardEvent<HTMLDivElement>) => {
              if (e.key === "Enter" && username !== "") {
                sendName();
              }
            }}
            onChange={handleChange}
            id="outlined-basic"
            label="Name"
            variant="outlined"
          />
          <Button
            onClick={sendName}
            variant="outlined"
            disabled={username === ""}
          >
            <SendIcon />
          </Button>
        </div>
      </div>
    </div>
  );
};
