<template>
  <div class="wrapper" @scroll="handleScroll">
    <SettingsModal
      v-if="showSettingsModal && isCurrentUser"
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
              <div v-if="isCurrentUser" class="setting-edit">
                <button @click="editProfile" class="edit-profile-button">
                  Edit Profile
                </button>
                <img
                  src="@/assets/settings.svg"
                  style="cursor: pointer"
                  @click="toggleSettingsModal"
                />
              </div>
              <div v-else>
                <button
                  v-if="isFriend"
                  class="friend-button"
                  @click="removeFriend"
                >
                  Friends
                </button>
                <button
                  v-else-if="friendRequestSent"
                  class="friend-button"
                  @click="cancelFriendRequest"
                >
                  Cancel
                </button>
                <button v-else class="friend-button" @click="addFriend">
                  Add Friend
                </button>
              </div>
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
            @click="activeTab = 'friends'"
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
            <button
              v-if="isCurrentUser"
              @click.stop="unfriend(friend.id)"
              class="unfriend-button"
            >
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
import { axiosInstance, endpoints } from "@/api/axiosHelper";
import Post from "@/components/Post.vue";
import SettingsModal from "@/components/SettingsModal.vue";

export default {
  components: {
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
      loading: false,
      page: 1,
      hasMore: true,
      showSettingsModal: false,
      isFriend: false,
      friendRequestSent: false,
      friendRequestId: null,
      currentUser: null,
    };
  },
  computed: {
    ...mapGetters(["getAuthToken"]),
    filteredFriends() {
      return this.friends.filter((friend) =>
        friend.username.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    isCurrentUser() {
      return this.currentUser && this.currentUser.id === this.user.id;
    },
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
    this.fetchCurrentUser();
    this.fetchUserProfile();
  },
  watch: {
    "$route.params.id": {
      handler() {
        this.fetchUserProfile();
      },
      immediate: true,
    },
    activeTab: {
      handler(newTab) {
        if (newTab === "friends") {
          this.fetchFriends();
        }
      },
      immediate: true,
    },
  },
  methods: {
    async fetchUserProfile() {
      try {
        const [userInfoResponse, friendsCountResponse] = await Promise.all([
          axiosInstance.get(
            `${endpoints.userProfile}${this.$route.params.id}/info/`
          ),
          axiosInstance.get(
            `${endpoints.friendsCount}?user_id=${this.$route.params.id}`
          ),
        ]);

        this.user = userInfoResponse.data;
        this.friendsCount = friendsCountResponse.data.friends_count;
        this.resetUserPosts(); // Reset userPosts when fetching new profile

        if (this.activeTab === "friends") {
          this.fetchFriends();
        }

        if (!this.isCurrentUser) {
          this.fetchFriendshipStatus();
        }
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    },

    resetUserPosts() {
      this.userPosts = [];
      this.page = 1;
      this.hasMore = true;
      this.fetchUserPosts();
    },
    async fetchFriendshipStatus() {
      try {
        const response = await axiosInstance.get(
          `${endpoints.friendshipStatus}${this.user.id}/friendship-status/`
        );
        this.isFriend = response.data.status === "friends";
        if (response.data.status === "requested") {
          this.friendRequestSent = true;
          this.friendRequestId = response.data.request_id;
        }
      } catch (error) {
        console.error("Error fetching friendship status:", error);
      }
    },
    async fetchCurrentUser() {
      try {
        const response = await axiosInstance.get(endpoints.currentUser);
        this.currentUser = response.data;
      } catch (error) {
        console.error("Error fetching current user data:", error);
      }
    },
    async fetchUserPosts() {
      if (this.loading || !this.hasMore) return;
      this.loading = true;

      try {
        const endpoint = this.isCurrentUser
          ? `${endpoints.myPosts}?page=${this.page}`
          : `${endpoints.posts}?user_id=${this.user.id}&page=${this.page}`;

        const response = await axiosInstance.get(endpoint);
        const newPosts = response.data.results;

        this.userPosts = [...this.userPosts, ...newPosts];

        if (!response.data.next) {
          this.hasMore = false;
        }

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
      } catch (error) {
        console.error("Error posting comment:", error);
      }
    },
    handleScroll(event) {
      const container = event.target;
      const scrollHeight = container.scrollHeight;
      const scrollTop = container.scrollTop;
      const clientHeight = container.clientHeight;

      const distanceFromBottom = scrollHeight - (scrollTop + clientHeight);
      const threshold = 0.1 * clientHeight;

      if (distanceFromBottom <= threshold) {
        this.fetchUserPosts();
      }
    },

    async cancelFriendRequest() {
      try {
        await axiosInstance.delete(
          `${endpoints.cancelFriendRequest}${this.friendRequestId}/`
        );
        this.friendRequestSent = false;
        this.friendRequestId = null;
      } catch (error) {
        console.error("Error canceling friend request:", error);
      }
    },
    async removeFriend() {
      try {
        await axiosInstance.delete(`${endpoints.removeFriend}${this.user.id}/`);
        this.isFriend = false;
      } catch (error) {
        console.error("Error removing friend:", error);
      }
    },
    async unfriend(friendId) {
      try {
        await axiosInstance.delete(`${endpoints.removeFriend}${friendId}/`);
        this.friends = this.friends.filter((friend) => friend.id !== friendId);
      } catch (error) {
        console.error("Error unfriending:", error);
      }
    },
    toggleSettingsModal() {
      this.showSettingsModal = !this.showSettingsModal;
    },
    goToFriendProfile(friendId) {
      this.$router.push({ name: "profile", params: { id: friendId } });
    },
    editProfile() {
      console.log("Navigating to edit profile page...");
      const userId = this.$route.params.id;
      console.log("User ID:", userId);
      this.$router.push({ name: "editProfile", params: { id: userId } });
    },
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.handleScroll);
  },
};
</script>

<style scoped>
.wrapper {
  display: flex;
  height: 100vh; /* Set wrapper height to full viewport height */
  position: relative;
  overflow-y: auto;
}

.content {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto; /* Center the content */
  height: 80vh;
  padding-top: 50px;
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

.setting-edit {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
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

.email {
  color: gray;
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
  padding: 5px 0 0 0;
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
  background-color: #efefef;
  border: none;
  color: black;
  border-radius: 4px;
  font-weight: bold;
}
.tabs button.active {
  background-color: #1e1e1e;
  color: white;
}

.tabs button:hover {
  background-color: #ddd;
  transform: scale(1.04);
}

.tabs button.active:hover {
  background-color: #555;
  color: white;
  transform: scale(1.04);
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

.friend-button {
  padding: 8px 17px;
  background-color: #efefef;
  color: #1e1e1e;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  margin-left: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: 600;
}

.friend-button:hover {
  background-color: #cfcfcf;
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

.edit-profile-button:hover {
  background-color: #cfcfcf;
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
</style>
