<template>
  <div class="wrapper">
    <NavBar />
    <SettingsModal
      v-if="showSettingsModal"
      :showModal="showSettingsModal"
      @close="toggleSettingsModal"
    />
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
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="54px"
                viewBox="0 -960 960 960"
                width="54px"
                fill="#000000"
                @click="toggleSettingsModal"
                style="cursor: pointer"
              >
                <path
                  d="m370-80-16-128q-13-5-24.5-12T307-235l-119 50L78-375l103-78q-1-7-1-13.5v-27q0-6.5 1-13.5L78-585l110-190 119 50q11-8 23-15t24-12l16-128h220l16 128q13 5 24.5 12t22.5 15l119-50 110 190-103 78q1 7 1 13.5v27q0 6.5-2 13.5l103 78-110 190-118-50q-11 8-23 15t-24 12L590-80H370Zm70-80h79l14-106q31-8 57.5-23.5T639-327l99 41 39-68-86-65q5-14 7-29.5t2-31.5q0-16-2-31.5t-7-29.5l86-65-39-68-99 42q-22-23-48.5-38.5T533-694l-13-106h-79l-14 106q-31 8-57.5 23.5T321-633l-99-41-39 68 86 64q-5 15-7 30t-2 32q0 16 2 31t7 30l-86 65 39 68 99-42q22 23 48.5 38.5T427-266l13 106Zm42-180q58 0 99-41t41-99q0-58-41-99t-99-41q-59 0-99.5 41T342-480q0 58 40.5 99t99.5 41Zm-2-140Z"
                />
              </svg>
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
          <div v-if="loading" class="loading-indicator">Loading...</div>
          <div v-if="!loading && !hasMore" class="end-of-feed">End of feed</div>
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
import { axiosInstance, endpoints } from "@/api/axiosHelper";
import SettingsModal from "@/components/SettingsModal.vue";

export default {
  components: {
    NavBar,
    Post,
    SettingsModal,
  },
  data() {
    return {
      user: null,
      userPosts: [],
      friends: [],
      searchQuery: "",
      friendsCount: 0,
      activeTab: "posts",
      commentText: "",
      loading: false,
      page: 1,
      hasMore: true,
      showSettingsModal: false,
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
    window.addEventListener("scroll", this.handleScroll);
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    async fetchCurrentUser() {
      try {
        const response = await axiosInstance.get(endpoints.currentUser);
        this.user = response.data;
        this.fetchFriendsCount();
        this.fetchUserPosts();
      } catch (error) {
        console.error("Error fetching current user data:", error);
      }
    },
    async fetchUserPosts() {
      if (this.loading || !this.hasMore) return;
      this.loading = true;

      try {
        const response = await axiosInstance.get(
          `${endpoints.myPosts}?page=${this.page}`
        );

        const newPosts = response.data.results;

        if (newPosts.length === 0 || response.data.next === null) {
          this.hasMore = false;
        }

        this.userPosts = [...this.userPosts, ...newPosts];
        this.page++;
      } catch (error) {
        console.error("Error fetching user's posts:", error);
      } finally {
        this.loading = false;
      }
    },
    async fetchFriendsCount() {
      try {
        const response = await axiosInstance.get(
          `${endpoints.friendsCount}?user_id=${this.user.id}`
        );
        this.friendsCount = response.data.friends_count;
      } catch (error) {
        console.error("Error fetching friends count:", error);
      }
    },
    async fetchFriends() {
      try {
        const response = await axiosInstance.get(
          `${endpoints.friends}?user_id=${this.user.id}`
        );
        this.friends = response.data;
      } catch (error) {
        console.error("Error fetching friends list:", error);
      }
    },
    async postComment(postId, commentText) {
      try {
        const response = await axiosInstance.post(endpoints.comments, {
          post: postId,
          text: commentText,
        });

        const newComment = response.data;
        newComment.date_time_created = new Date(newComment.date_time_created);

        const updatedPosts = this.userPosts.map((post) => {
          if (post.id === postId) {
            post.comments.unshift(newComment);
          }
          return post;
        });

        this.userPosts = updatedPosts;
        this.commentText = ""; // Clear the input field
      } catch (error) {
        console.error("Error posting comment:", error);
      }
    },

    handleScroll() {
      if (this.loading || !this.hasMore) return;

      const scrollHeight = document.documentElement.scrollHeight;
      const scrollTop =
        document.documentElement.scrollTop || document.body.scrollTop;
      const clientHeight = window.innerHeight;

      if (scrollTop + clientHeight >= scrollHeight - 100) {
        this.fetchUserPosts();
      }
    },
    toggleSettingsModal() {
      this.showSettingsModal = !this.showSettingsModal;
    },
    editProfile() {
      this.$router.push("/myprofile/edit");
    },
    goToFriendProfile(friendId) {
      this.$router.push({ name: "profile", params: { id: friendId } });
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
  background-color: #efefef;
  color: #363636;
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
  background-color: #cfcfcf;
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
  font-size: 20px;
  padding: 16px 0 0 0;
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
