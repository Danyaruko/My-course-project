import React, { useState, useEffect } from "react";
import { getAllTankStatuses, getCurrTankStatus } from "../../service/api";
import "./TankState.css";

const TankState = () => {
  const [data, setData] = useState([]);
  const [viewMode, setViewMode] = useState(false);

  const getData = async () => {
    if (viewMode) {
      const data = await getAllTankStatuses();
      setData(data);
    } else {
      const data = await getCurrTankStatus();
      setData(data);
    }
  };
  useEffect(() => {
    getData();
  }, []);

  useEffect(() => {
    getData();
  }, [viewMode]);

  console.log(data);
  const handleTimeReveceived = (item) => {
    const dateTime = item.time.split("T");
    const date = dateTime[0];
    const time = dateTime[1];
    console.log(date, time);
    return { date, time };
  };
  return (
    <div className="tank">
      <h1>Tank Status</h1>
      <div>
        <button className="switch" onClick={() => setViewMode(!viewMode)}>
          {viewMode ? "See Current State" : "See All States"}
        </button>
      </div>
      <div>
        {data &&
          data.map((item) => {
            const dateTime = handleTimeReveceived(item);
            return (
              <div className="tank__info">
                <div>{item.state}</div>
                <div>
                  {dateTime.date} | {dateTime.time}
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default TankState;
