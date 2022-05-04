import {
  Toolbar,
  CircularProgress,
  Button,
  AppBar,
  Typography,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import GitHubIcon from "@mui/icons-material/GitHub";
import { useCallback } from "react";
import { useEffect, useState } from "react";

export const MainApp = () => {
  const [imgCount, setImgCount] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadingNew, setLoadingNew] = useState<boolean>(false);
  const [blobs, setBlobs] = useState<string[]>([]);
  const [blobsCount, setBlobsCount] = useState<number>(1);

  useEffect(() => {
    const getImgs = async (id: number) =>
      await fetch("http://localhost:8000/Show/" + id, {
        mode: 'cors',
        credentials: "include",
      })
        .then((response) => response.blob())
        .then((data) => {
          setBlobs([...blobs, URL.createObjectURL(data)]);
          setBlobsCount(blobsCount + 1);
        });

    const getRes = async () => {
      if (imgCount > 0 && blobsCount <= imgCount) {
        getImgs(blobsCount);
      } else {
        await fetch("http://localhost:8000/GetImagesCount", {
          mode: 'cors',
          credentials: "include",
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data);

            setImgCount(data.count);
            if (imgCount > 0 && blobsCount <= imgCount) {
              getImgs(blobsCount);
            }
            setLoading(false);
          });
      }
    };
    getRes();
  }, [imgCount, blobsCount]);

  const addNewPic = useCallback(async () => {
    setLoadingNew(true);
    await fetch("http://localhost:8000/New", {
      mode: 'cors',
      credentials: "include",
    })
      .then((response) => response.blob())
      .then((data) => {
        setBlobs([...blobs, URL.createObjectURL(data)]);
        setLoadingNew(false);
      });
  }, [blobs]);

  return (
    <div className="App">
      <AppBar position="static">
        <Toolbar>
          <div>
            <form action="https://github.com/NabilNYMansour/Maze-Gen-Web-App">
              <a href="https://github.com/NabilNYMansour/Maze-Gen-Web-App">
                <button type="submit" className="topnavbutton">
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
        </Toolbar>
      </AppBar>
      {loading ? (
        <div className="loading">
          <CircularProgress />
        </div>
      ) : (
        <div className="pictures">
          {blobs.map((blob, i) => (
            <img className="picture" key={i} alt="a maze" src={blob}></img>
          ))}
          <div className="picture">
            <div className="new-button-container">
              {loadingNew ? (
                <CircularProgress />
              ) : (
                <Button variant="contained" onClick={() => addNewPic()}>
                  <AddIcon />
                </Button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
