// One place that knows the backend URL. Every API call goes through here.
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export default api;
