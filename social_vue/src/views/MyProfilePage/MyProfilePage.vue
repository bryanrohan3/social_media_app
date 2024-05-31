<template>
  <div class="wrapper">
    <NavBar />
    <div class="content">
      <div class="profile-page" v-if="user">
        <!-- Profile header -->
        <div class="profile-header">
          <!-- Avatar -->
          <img
            :src="user.avatar || 'https://via.placeholder.com/150'"
            alt="User Avatar"
            class="profile-avatar"
          />
          <!-- Profile info -->
          <div class="profile-info">
            <div class="info-top">
              <h1 class="username">{{ user.username }}</h1>
              <button @click="editProfile" class="edit-profile-button">
                Edit Profile
              </button>
            </div>
            <p class="name">{{ user.first_name }} {{ user.last_name }}</p>
            <!-- <p class="email">{{ user.email }}</p> -->
            <p class="email">Friends · 12</p>
          </div>
        </div>

        <!-- Display user's posts using the Post component -->
      </div>
      <Post :posts="userPosts" class="post-content" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import NavBar from "@/components/NavBar.vue";
import Post from "@/components/Post.vue";

export default {
  components: {
    NavBar,
    Post,
  },
  data() {
    return {
      user: null,
      userPosts: [],
    };
  },
  computed: {
    ...mapGetters(["getAuthToken"]),
  },
  mounted() {
    this.fetchCurrentUser();
    this.fetchUserPosts();
  },
  methods: {
    async fetchCurrentUser() {
      try {
        const token = this.getAuthToken;
        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };
        const response = await axios.get(
          "http://127.0.0.1:8000/api/users/current/",
          config
        );
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching current user data:", error);
      }
    },
    async fetchUserPosts() {
      try {
        const token = this.getAuthToken;
        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };
        const response = await axios.get(
          "http://127.0.0.1:8000/api/posts/my_posts/",
          config
        );
        this.userPosts = response.data;
      } catch (error) {
        console.error("Error fetching user's posts:", error);
      }
    },

    editProfile() {
      // Logic for editing the profile
    },
    formatDate(dateString) {
      const date = new Date(dateString);

      const day = date.getDate();
      const month = date.toLocaleString("default", { month: "long" });
      const hour = date.getHours();
      const minute = date.getMinutes();
      const period = hour >= 12 ? "PM" : "AM";
      const formattedHour = hour > 12 ? hour - 12 : hour;
      const formattedMinute = minute < 10 ? `0${minute}` : minute;

      return `${day}th ${month} at ${formattedHour}:${formattedMinute}${period}`;
    },
  },
};
</script>

<style scoped>
.wrapper {
  display: flex;
  height: 100vh; /* Set wrapper height to full viewport height */
  position: relative;
}

.content {
  /* Remove overflow-y: auto; */
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.post-content {
  margin-top: 40px;
  display: flex;
}

.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 100px;
}

.profile-header {
  display: flex;
  align-items: center;
}

.profile-avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-info {
  text-align: left;
}

.info-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.profile-info h1 {
  margin: 0;
}

.profile-info p {
  margin: 5px 0;
}

.edit-profile-button {
  padding: 8px 18px;
  font-size: 16px;
  cursor: pointer;
  background-color: #363636;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  margin-left: 10px;
  transition: background-color 0.3s ease;
}

.email {
  color: gray;
}

.edit-profile-button:hover {
  background-color: #1e1e1e;
  text-shadow: #363636 1px 0 10px;
}

@media screen and (max-width: 768px) {
  .line-divider {
    display: none; /* Hide the line divider on smaller screens */
  }
}

/* user posts */
.user-posts {
  margin-top: 20px;
}

.post {
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 20px;
  display: flex; /* Ensure the post content is flex */
  flex-direction: column; /* Arrange the content vertically */
  width: 450px;
  margin-bottom: 20px; /* Add margin-bottom */
}

.post-header {
  display: flex;
  align-items: center; /* Center items horizontally */
  gap: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.user-info {
  display: flex;
  flex-direction: column; /* Arrange the username and date vertically */
}

.username {
  font-weight: bold;
  margin: 0;
  align-self: start;
}

.date {
  color: #555;
  font-size: 0.8rem;
  margin: 0;
}

.caption {
  margin-top: 20px;
  align-self: start;
}

.created-at {
  color: #555;
  font-size: 0.8rem;
  margin-top: 10px;
}
</style>
