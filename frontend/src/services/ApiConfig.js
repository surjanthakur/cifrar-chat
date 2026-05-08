import axios from "axios";

const Base_api_url = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true,
});

export default Base_api_url;
