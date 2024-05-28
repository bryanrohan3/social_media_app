<template>
  <div class="navbar-wrapper" :class="{ active: showSearchInput }">
    <!-- Add an overlay to capture clicks outside the search container -->
    <div v-if="showSearchInput" class="overlay" @click="closeSearchInput"></div>
    <div class="navbar">
      <p class="dancing-script">iSocial</p>
      <div class="nav-item">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          fill="#000000"
        >
          <path
            d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"
          />
        </svg>
        <router-link to="/">Home</router-link>
      </div>
      <div class="nav-item" @click="toggleSearchInput">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          fill="#000000"
        >
          <path
            d="M784-120 532-372q-30 24-69 38t-83 14q-109 0-184.5-75.5T120-580q0-109 75.5-184.5T380-840q109 0 184.5 75.5T640-580q0 44-14 83t-38 69l252 252-56 56ZM380-400q75 0 127.5-52.5T560-580q0-75-52.5-127.5T380-760q-75 0-127.5 52.5T200-580q0 75 52.5 127.5T380-400Z"
          />
        </svg>
        <a>Search</a>
      </div>
      <div class="nav-item">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          fill="#000000"
        >
          <path
            d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0-60Zm0 360Z"
          />
        </svg>
        <router-link to="#">Profile</router-link>
      </div>
      <button
        class="logout-button"
        v-if="userProfile && userProfile.token"
        @click="handleLogout"
      >
        Logout
      </button>
      <button class="login-button" v-else @click="redirectToLogin">
        Login
      </button>
    </div>
    <div v-if="showSearchInput" class="search-container">
      <p class="SearchHeader">Search</p>
      <input
        type="text"
        v-model="searchQuery"
        @input="debouncedSearch"
        placeholder="Search user profiles..."
      />
      <ul v-if="searchResults.length">
        <li v-for="user in searchResults" :key="user.id">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
            fill="#000000"
          >
            <path
              d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0-60Zm0 360Z"
            />
          </svg>

          <div class="username-details">
            <p class="username">{{ user.username }}</p>
            <p class="name">{{ user.first_name }} {{ user.last_name }}</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
import { debounce } from "lodash";
import axios from "axios";

export default {
  data() {
    return {
      showSearchInput: false,
      searchQuery: "",
      searchResults: [],
    };
  },
  computed: {
    ...mapGetters(["getUserProfile", "getAuthToken"]),
    userProfile() {
      return this.getUserProfile;
    },
  },
  methods: {
    ...mapMutations(["logout"]),
    handleLogout() {
      this.logout();
      this.$router.push("/login");
    },
    redirectToLogin() {
      this.$router.push("/login");
    },
    toggleSearchInput() {
      this.showSearchInput = !this.showSearchInput;
    },
    debouncedSearch: debounce(async function () {
      if (!this.userProfile || !this.userProfile.token) {
        return;
      }

      if (this.searchQuery.trim() === "") {
        this.searchResults = [];
        return;
      }

      try {
        const token = this.userProfile.token;
        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };

        const response = await axios.get(
          `http://127.0.0.1:8000/api/users/?query=${this.searchQuery}`,
          config
        );
        this.searchResults = response.data;
      } catch (error) {
        console.error("Error searching for users:", error);
      }
    }, 500),
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap");

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: #f9f9fd;
}

.dancing-script {
  font-family: "Dancing Script", cursive;
  font-optical-sizing: auto;
  margin-right: 100%;
  font-weight: 800;
  font-size: 40px;
  font-style: normal;
}

.iSocial {
  font-size: 20px;
  font-weight: bold;
}

.home {
  display: flex;
  height: 100vh;
}

.navbar-wrapper {
  position: relative;
  height: 100%;
}

.navbar {
  width: 200px; /* Adjust width as needed */
  background-color: #f9f9fd; /* Example background color */
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  padding: 20px;
  transition: width 0.5s;
  overflow: hidden;
  border-right: 1px solid #e9e9e5;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.nav-item {
  display: flex;
  align-items: center;
  margin-bottom: 40px; /* Increased spacing between items */
  cursor: pointer;
}

.nav-item svg {
  margin-right: 10px;
}

.navbar a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 18px;
}

.search-container {
  position: fixed;
  top: 0;
  left: 200px; /* Start from where the navbar ends */
  width: 300px;
  height: 100%;
  background-color: #f9f9fd;
  border-right: #e9e9e5 solid 1px;
  transform: translateX(100%);
  transition: transform 0.5s ease; /* Transition for sliding effect */
  display: flex;
  flex-direction: column;
  padding: 20px; /* Add padding to avoid overlap */
  box-sizing: border-box; /* Include padding in width calculation */
}

.search-container input {
  width: 100%; /* Adjust width to account for padding */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Ensure padding is included in the width */
}

.search-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-container li {
  padding: 10px;
  border-bottom: 1px solid #e9e9e5;
}

.search-container li:hover {
  background-color: #f1f1f1;
}

.search-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-container li {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #e9e9e5;
}

.search-container li svg {
  margin-right: 10px;
}

.search-container li .details {
  display: flex;
  flex-direction: column;
}

.search-container li .details p {
  margin: 0;
}

.search-container li .details p:first-child {
  font-weight: bold;
  color: black; /* Set color to black */
  font-size: 16px; /* Set font size */
}

.search-container li .details p:last-child {
  font-size: 14px; /* Set smaller font size */
  color: gray; /* Set color to gray */
}

.search-container li .username-details {
  display: flex;
  flex-direction: column;
}

.search-container li .username-details p {
  margin: 0;
}

.search-container li .username-details .username {
  font-weight: bold;
  color: black;
  font-size: 16px;
}

.search-container li .username-details .name {
  font-size: 14px;
  color: gray;
  margin-left: 5px; /* Add some spacing between username and name */
}

.navbar-wrapper.active .search-container {
  transform: translateX(0); /* Slide in from the right when active */
}

.content {
  flex: 1;
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 2rem;
  margin-left: 200px; /* Make space for fixed navbar */
}

h1 {
  font-family: "Arial", sans-serif;
  font-size: 2rem;
  color: #333;
}

button {
  padding: 0.85rem 1rem;
  background-color: #27282a; /* Set the background color */
  color: #fff;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  border-radius: 10px;
}

.logout-button {
  margin-top: auto;
}

.login-button {
  margin-top: auto;
}
</style>
