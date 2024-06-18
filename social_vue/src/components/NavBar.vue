<template>
  <div class="navbar-wrapper" :class="{ active: showSearchInput }">
    <div
      v-if="showSearchInput"
      class="search-container"
      @click="closeSearchInput"
    ></div>
    <div class="navbar">
      <p class="dancing-script">iSocial</p>
      <router-link to="/">
        <div class="nav-item">
          <img src="@/assets/home.svg" class="icon" />
          <a href="/">Home</a>
        </div>
      </router-link>

      <a class="nav-item" @click="toggleSearchInput">
        <img src="@/assets/search.svg" class="icon" />
        <a>Search</a>
      </a>

      <div class="nav-item" @click="openCreatePostModal">
        <img src="@/assets/create.svg" class="icon" />
        <a>Create</a>
      </div>

      <router-link to="/friend-requests" exact>
        <div class="nav-item">
          <img src="@/assets/friends.svg" class="icon" />
          <a>Friends</a>
        </div>
      </router-link>

      <router-link to="/myprofile" exact>
        <div class="nav-item">
          <img src="@/assets/account_profile.svg" class="icon" />
          Profile
        </div>
      </router-link>

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

    <transition name="slide-fade">
      <div v-if="showSearchInput" class="search-container">
        <p class="SearchHeader">Search</p>
        <input
          type="text"
          v-model="searchQuery"
          @input="debouncedSearch"
          placeholder="Search user profiles..."
        />
        <table v-if="searchResults.length">
          <tbody>
            <tr
              v-for="user in searchResults"
              :key="user.id"
              @click="goToUserProfile(user.id)"
              class="user-row"
            >
              <td class="avatar-cell">
                <img
                  src="@/assets/avatar.jpeg"
                  alt="Avatar"
                  class="avatar-search"
                />
              </td>
              <td class="user-details">
                <p class="username">{{ user.username }}</p>
                <p class="name">{{ user.first_name }} {{ user.last_name }}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </transition>

    <CreatePostModal
      v-if="showCreatePostModal"
      @close="showCreatePostModal = false"
    />
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
import { debounce } from "lodash";
import CreatePostModal from "@/components/CreatePostModal.vue";
import router from "@/router";
import axiosInstance from "@/api/axiosHelper";

export default {
  data() {
    return {
      showSearchInput: false,
      showCreatePostModal: false,
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
  components: {
    CreatePostModal,
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
    openCreatePostModal() {
      this.showCreatePostModal = true;
    },
    toggleSearchInput() {
      this.showSearchInput = !this.showSearchInput;
    },
    goToUserProfile(userId) {
      // Navigate to the user profile page with the user's ID as a route parameter
      this.$router.push({ name: "profile", params: { id: userId } });
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

        const response = await axiosInstance.get(
          `http://127.0.0.1:8000/api/users/?query=${this.searchQuery}`
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
  background-color: #ffffff;
}

.icon {
  margin-right: 10px;
}

.dancing-script {
  font-family: "Dancing Script", cursive;
  font-optical-sizing: auto;
  margin-right: 100%;
  font-weight: 800;
  font-size: 40px;
  font-style: normal;
  margin-left: 20px;
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
  background-color: #ffffff; /* Example background color */
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
  cursor: pointer;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  color: #333;
}

.nav-item:hover {
  background-color: #f1f1f1;
}

.nav-item svg {
  margin-right: 10px;
}

.navbar a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 16px;
}

.search-container input,
.search-container li {
  width: 100%; /* Adjust width to account for padding */
  padding: 10px;
  box-sizing: border-box; /* Ensure padding is included in the width */
}

.search-container li:hover {
  background-color: #f1f1f1;
}

.search-container input {
  outline: none;
  font-size: 16px;
  width: 100%; /* Adjust width to account for padding */
  padding: 10px;
  box-sizing: border-box; /* Ensure padding is included in the width */
  border-radius: 10px;
  border: 1px solid #e9e9e5;
}

.search-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-container li {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e9e9e5;
}

.search-container li svg {
  margin-right: 10px;
}

.search-container li .details,
.search-container li .username-details {
  display: flex;
  flex-direction: column;
}

.search-container li .details p,
.search-container li .username-details p {
  margin: 0;
}

.search-container li .details p:first-child,
.search-container li .username-details .username {
  font-weight: bold;
  color: black;
  font-size: 16px;
  align-items: start;
}

.search-container li .details p:last-child,
.search-container li .username-details .name {
  font-size: 14px;
  color: gray;
  align-items: start;
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

.logout-button,
.login-button {
  margin-top: auto;
}

button:hover {
  background-color: #363636; /* Set darker background color on hover */
}

.nav-item .icon {
  transition: transform 0.3s ease;
}

.nav-item:hover .icon {
  transform: scale(1.1);
}

.search-container-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 299;
}

/* New styles */
.search-container {
  position: fixed;
  top: 0;
  left: 220px; /* Adjust to your navbar width */
  width: 300px;
  height: 100%;
  background-color: #ffffff;
  border-right: 1px solid #e9e9e5;
  z-index: 300;
  overflow: hidden;
  padding: 20px;
  box-sizing: border-box;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-fade-enter-to,
.slide-fade-leave-from {
  transform: translateX(0%);
  opacity: 1;
}

/* table style */

.SearchHeader {
  font-size: 1.2em;
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

.user-row {
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.user-row:hover {
  background-color: #f9f9f9;
}

.avatar-cell {
  width: 50px;
  padding-right: 10px;
}

.avatar-search {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: 1px solid gray;
}

.user-details {
  flex: 1;
}

.username {
  font-weight: bold;
  font-size: 0.9em;
  margin: auto 0;
}

.name {
  font-size: 0.8em;
  color: #555;
  margin: 0;
  margin-top: 10px;
}
</style>
