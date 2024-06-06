<template>
  <div class="wrapper">
    <NavBar />
    <div class="content">
      <div class="profile-page" v-if="user">
        <!-- Profile header -->
        <div class="profile-header">
          <!-- Avatar -->
          <img class="profile-avatar" src="@/assets/avatar.jpeg" alt="Avatar" />
          <!-- Profile info -->
          <div class="profile-info">
            <div class="info-top">
              <h1 class="username">{{ user.username }}</h1>
              <button @click="editProfile" class="edit-profile-button">
                Edit Profile
              </button>
            </div>
            <p class="name">{{ user.first_name }} {{ user.last_name }}</p>
            <p class="email">Friends · {{ friendsCount }}</p>
          </div>
        </div>

        <!-- Tabs for posts and friends -->
        <div class="tabs">
          <button
            :class="{ active: activeTab === 'posts' }"
            @click="activeTab = 'posts'"
          >
            Posts
          </button>
          <button
            :class="{ active: activeTab === 'friends' }"
            @click="
              activeTab = 'friends';
              fetchFriends();
            "
          >
            Friends
          </button>
        </div>

        <!-- Content based on active tab -->
        <div v-if="activeTab === 'posts'">
          <Post
            :posts="userPosts"
            :post-comment="postComment"
            class="post-content"
          />
        </div>
        <div v-if="activeTab === 'friends'" class="tab-content">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search by username"
            class="search-input"
          />
          <div
            v-for="friend in filteredFriends"
            :key="friend.id"
            class="friend-item"
            @click="goToFriendProfile(friend.id)"
          >
            <img
              class="friend-avatar"
              src="@/assets/avatar.jpeg"
              alt="Avatar"
            />
            <div class="friend-info">
              <p class="friend-username">{{ friend.username }}</p>
              <p class="friend-name">
                {{ friend.first_name }} {{ friend.last_name }}
              </p>
            </div>
            <button @click.stop="unfriend(friend.id)" class="unfriend-button">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 -960 960 960"
                width="24px"
                fill="#c70000"
              >
                <path
                  d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import NavBar from "@/components/NavBar.vue";
import Post from "@/components/Post.vue";
import axiosInstance from "@/api/axiosHelper"; // Import Axios instance

export default {
  components: {
    NavBar,
    Post,
  },
  data() {
    return {
      user: null,
      userPosts: [],
      friends: [],
      searchQuery: "",
      friendsCount: 0,
      activeTab: "posts", // Set default tab to 'posts'
      commentText: "",
    };
  },
  computed: {
    ...mapGetters(["getAuthToken"]),
    filteredFriends() {
      // Filter friends based on search query
      return this.friends.filter((friend) =>
        friend.username.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  mounted() {
    this.fetchCurrentUser();
  },
  methods: {
    async fetchCurrentUser() {
      try {
        const response = await axiosInstance.get(
          "http://127.0.0.1:8000/api/users/current/"
        );
        this.user = response.data;
        this.fetchFriendsCount();
        this.fetchUserPosts();
      } catch (error) {
        console.error("Error fetching current user data:", error);
      }
    },
    async fetchUserPosts() {
      try {
        const response = await axiosInstance.get(
          "http://127.0.0.1:8000/api/posts/my_posts/"
        );
        const userPosts = response.data.map(async (post) => {
          try {
            const commentsResponse = await axiosInstance.get(
              `http://127.0.0.1:8000/api/comments/?post_id=${post.id}&latest=true`
            );
            post.comments = commentsResponse.data;
          } catch (error) {
            console.error(
              `Error fetching comments for post ${post.id}:`,
              error
            );
            post.comments = [];
          }
          return post;
        });

        this.userPosts = await Promise.all(userPosts);
      } catch (error) {
        console.error("Error fetching user's posts:", error);
      }
    },
    async fetchFriendsCount() {
      try {
        const response = await axiosInstance.get(
          `http://127.0.0.1:8000/api/friend-requests/friends/?user_id=${this.user.id}`
        );
        this.friendsCount = response.data.length;
      } catch (error) {
        console.error("Error fetching friends count:", error);
      }
    },
    async unfriend(friendId) {
      try {
        const response = await axiosInstance.delete(
          `http://127.0.0.1:8000/api/friend-requests/unfriend/${friendId}/`
        );
        // Assuming the API returns success if the unfriend action is successful
        if (response.status === 200) {
          // Update the friends list after unfriending
          this.fetchFriends();
        }
      } catch (error) {
        console.error("Error unfriending:", error);
      }
    },
    async fetchFriends() {
      try {
        const response = await axiosInstance.get(
          `http://127.0.0.1:8000/api/friend-requests/friends/?user_id=${this.user.id}`
        );
        this.friends = response.data;
      } catch (error) {
        console.error("Error fetching friends list:", error);
      }
    },
    async postComment(postId, commentText) {
      try {
        await axiosInstance.post("http://127.0.0.1:8000/api/comments/", {
          post: postId,
          text: commentText,
        });
        // Clear the comment text area after posting
        this.commentText = "";
        // Update the posts to reflect the new comment
        this.fetchUserPosts();
      } catch (error) {
        console.error("Error posting comment:", error);
      }
    },
    editProfile() {
      this.$router.push("/myprofile/edit");
    },
    goToFriendProfile(friendId) {
      this.$router.push({ name: "profile", params: { id: friendId } });
    },
    formatDate(dateString) {
      const date = new Date(dateString);

      const day = date.getDate();
      const month = date.toLocaleString("default", { month: "long" });
      const hour = date.getHours();
      const minute = date.getMinutes();
      const ampm = hour >= 12 ? "PM" : "AM";

      return `${day} ${month} at ${hour % 12}:${minute
        .toString()
        .padStart(2, "0")} ${ampm}`;
    },
  },
};
</script>

<style scoped>
/* Add styles here */
</style>

<style scoped>
.wrapper {
  display: flex;
  height: 100vh; /* Set wrapper height to full viewport height */
  position: relative;
}

.content {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto; /* Center the content */
}

.post-content {
  margin-top: 40px;
  display: flex;
  margin: auto 0;
  margin-top: 40px;
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

/* Tabs */
.tabs {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.tabs button {
  padding: 10px 20px;
  margin: 0 10px;
  cursor: pointer;
  background-color: lightgrey;
  border: none;
  border-radius: 4px;
  font-weight: bold;
}
.tabs button.active {
  background-color: #1e1e1e;
  color: white;
}

/* Friend list */

.tab-content {
  margin-top: 20px;
}

.friend-item {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;

  border-radius: 10px;
  width: 100%;
  max-width: 600px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  width: 500px;
}

.friend-item:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.unfriend-button {
  margin-left: auto; /* Align the unfriend button to the right */
  padding: 8px 18px;
  font-size: 16px;
  cursor: pointer;
  background-color: #fff; /* Red color for the unfriend button */
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  transition: background-color 0.3s ease;
  width: 100px;
}

.unfriend-button:hover {
  background-color: #f0f0f0; /* Darker red color on hover */
  cursor: pointer;
}

.friend-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-right: 20px;
  object-fit: cover;
}

.friend-info {
  display: flex;
  flex-direction: column;
}

.friend-username {
  font-weight: bold;
  margin: 0;
  font-size: 1.1em;
  align-items: start;
}

.friend-name {
  margin: 0;
  color: gray;
  align-self: start;
  font-size: 0.9em;
}

.search-input {
  margin-bottom: 20px;
  padding: 10px;
  width: 100%;
  max-width: 400px;
  border: 1px solid #fff;
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
}
</style>
