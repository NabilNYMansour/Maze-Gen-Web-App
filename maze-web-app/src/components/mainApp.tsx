import {
  CircularProgress,
  Button,

} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import { useCallback } from "react";
import { useEffect, useState } from "react";

export const getColor = (role : string) => role === "admin" ? "success" : role === "creator" ? "secondary" : "primary";
export const getColorCode = (role : string) => role === "admin" ? "#388e3c" : role === "creator" ? "#ab47bc" : role === "viewer" ? "#1976d2" : "#989898";
export const getColorCodeLighter = (role : string) => role === "admin" ? "#9ffba4" : role === "creator" ? "#ed95fd" : role === "viewer" ? "#8cc6ff" : "#b9b9b9";

export const MainApp = ({ role }: { role: string }) => {
  const [imgList, setImgList] = useState<number[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadingNew, setLoadingNew] = useState<boolean>(false);
  const [blobs, setBlobs] = useState<string[]>([]);
  const [currentBlobCount, setCurrentBlobCount] = useState<number>(0);
  const [currentBlobIndex, setCurrentBlobIndex] = useState<number>(-1);
  const [highLightedImg, setHighLightedImg] = useState<number>(-1);

  useEffect(() => {
    const getImgList = async () => {
      if (loading) {
        await fetch("http://localhost:8000/GetImgList", {
          mode: "cors",
          credentials: "include",
        })
          .then((response) => response.json())
          .then((data) => {
            setImgList(data);
            setLoading(imgList.length === 0);
            if (imgList.length !== 0) {
              setCurrentBlobCount(imgList[0]);
              setCurrentBlobIndex(0);
            }
          });
      }
    };

    const getImgsCount = async () => {
      await fetch("http://localhost:8000/GetImagesCount", {
        mode: "cors",
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.count !== 0) {
            getImgList();
          } else {
            setLoading(false);
          }
        });
    };

    getImgsCount();
  }, [imgList, loading]);

  useEffect(() => {
    const getImg = async (id: number) => {
      if (currentBlobIndex !== imgList.length && !loading) {
        await fetch("http://localhost:8000/Show/" + id, {
          mode: "cors",
          credentials: "include",
        })
          .then((response) => response.blob())
          .then((data) => {
            if (data.type === "image/jpeg") {
              setBlobs([...blobs, URL.createObjectURL(data)]);
              setCurrentBlobIndex(currentBlobIndex + 1);
              setCurrentBlobCount(imgList[currentBlobIndex]);
            }
          });
      }
    };

    getImg(currentBlobCount);
  }, [currentBlobCount, currentBlobIndex, loading]);

  const addNewPic = useCallback(async () => {
    setLoadingNew(true);
    await fetch("http://localhost:8000/New", {
      mode: "cors",
      credentials: "include",
    })
      .then((response) => response.blob())
      .then((data) => {
        setBlobs([...blobs, URL.createObjectURL(data)]);
        setLoadingNew(false);
        imgList.length > 0
          ? setImgList([...imgList, imgList[imgList.length - 1] + 1])
          : setImgList([1]);
      });
  }, [blobs, imgList]);

  const removePic = useCallback(
    async (index: number) => {
      await fetch("http://localhost:8000/Delete/" + imgList[index], {
        mode: "cors",
        credentials: "include",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          setImgList(imgList.filter((_, i) => i !== index));
          setBlobs(blobs.filter((_, i) => i !== index));
        });
    },
    [blobs, imgList]
  );

  return (
    <div>
      {loading ? (
        <div className="loading">
          <CircularProgress color={getColor(role)}/>
        </div>
      ) : (
        <div className="pictures">
          {blobs.map((blob, i) => (
            <div className="img-container" key={i}>
              <img
                onMouseEnter={() => {
                  if (role === "admin") {
                    setHighLightedImg(i);
                  }
                }}
                onMouseLeave={() => {
                  if (role === "admin") {
                    setHighLightedImg(-1);
                  }
                }}
                className={
                  role === "admin" || highLightedImg !== i
                    ? ""
                    : "hover-over-img"
                }
                key={i}
                alt="a maze"
                src={blob}
              ></img>
              {role === "admin" ? (
                <div
                  onMouseEnter={() => {
                    setHighLightedImg(i);
                  }}
                  hidden={highLightedImg !== i}
                >
                  <Button
                    onClick={() => removePic(i)}
                    className="remove-button"
                    variant="contained"
                    color={getColor(role)}
                  >
                    <RemoveIcon />
                  </Button>
                </div>
              ) : (
                ""
              )}
            </div>
          ))}
          <div>
            <div className="new-button-container">
              {loadingNew ? (
                <CircularProgress />
              ) : (
                <Button
                  disabled={role === "viewer"}
                  variant="contained"
                  onClick={() => addNewPic()}
                  color={getColor(role)}
                >
                  <AddIcon />
                </Button>
              )}
            </div>
          </div>
        </div>
      )}
      {/* <button
        onClick={() => {
          console.log(imgList);
        }}
      >
        TEST
      </button> */}
    </div>
  );
};
