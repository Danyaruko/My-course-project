import axios from "axios";

const http = axios.create({
  baseURL: "http://localhost:5000/",
  headers: { "Content-type": "application-json" },
});

export const getCurrTankStatus = async () => {
  let url = "http://localhost:5000/" + "tank_state_last";
 const data = (await http.get(url)).data
 console.log(data)
  return data;
};

export const getAllTankStatuses = async () => {
  let url = "http://localhost:5000/" + "tank_state";
  const data = (await http.get(url)).data
  return data;
};
