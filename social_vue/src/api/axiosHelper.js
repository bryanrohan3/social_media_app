// axiosHelper.js
import axios from "axios";
import store from "@/store"; // Assuming your Vuex store is configured

const hostname = "http://localhost:8000/";

const apiConstants = {
  api_hostname: hostname + "api/",
  hostname: hostname,
};

const axiosInstance = axios.create({
  baseURL: apiConstants.api_hostname, // Your API base URL
});

let tokenType = "Token";

// Add a request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const token = store.getters.getAuthToken; // Get the token from your Vuex store
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

const endpoints = {
  login: apiConstants.api_hostname + "users/login/",
  signup: apiConstants.api_hostname + "users/", // Endpoint for user signup
  posts: apiConstants.api_hostname + "posts/", // Base URL for posts
  myPosts: apiConstants.api_hostname + "posts/my_posts/",
  userPosts: apiConstants.api_hostname + "posts/", // For fetching posts by user ID
  comments: apiConstants.api_hostname + "comments/", // Base URL for comments
  likes: apiConstants.api_hostname + "likes/",
  unlike: apiConstants.api_hostname + "likes/", // Ensure this is the correct endpoint
  currentUser: apiConstants.api_hostname + "users/current/",
  userProfile: apiConstants.api_hostname + "users/",
  updateUser: apiConstants.api_hostname + "users/", // For updating user profile
  friendshipStatus: apiConstants.api_hostname + "friend-requests/",
  friendRequests: apiConstants.api_hostname + "friend-requests/",
  friendsCount: apiConstants.api_hostname + "friend-requests/friends_count/",
  friends: apiConstants.api_hostname + "friend-requests/friends/",
  unfriend: apiConstants.api_hostname + "friend-requests/unfriend/",
  pendingRequests:
    apiConstants.api_hostname + "friend-requests/pending_requests/", // For pending friend requests
};

export { axiosInstance, endpoints };
