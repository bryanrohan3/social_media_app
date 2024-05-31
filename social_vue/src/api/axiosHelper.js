// axios.js
import axios from "axios";
import store from "@/store"; // Assuming your Vuex store is configured

const axiosInstance = axios.create({
  //   baseURL: "http://127.0.0.1:8000", // Your API base URL
});

let tokenType = "Token";

// Add a request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const token = store.getters.getAuthToken; // Get the token from your Vuex store
    console.log("Auth Token:", token);

    if (token) {
      config.headers["Authorization"] = `${tokenType} ${token}`; // Set the token in the Authorization header
    } else {
      console.warn("No auth token found");
    }

    return config;
  },
  (error) => {
    return Promise.reject(error); // Pass the error to the next interceptor
  }
);

export default axiosInstance;
