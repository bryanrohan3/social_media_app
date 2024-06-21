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
      activeTab: "posts",
      isFriend: false,
      friendRequestSent: false,
      friendRequestId: null,
      currentUser: null,
      page: 1,
      hasMore: true,
      loading: false, // Add loading state to prevent concurrent requests
    };
  },
  computed: {
    ...mapGetters(["getAuthToken"]),
    filteredFriends() {
      return this.friends.filter((friend) =>
        friend.username.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
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
        const response = await axiosInstance.get(
          `${endpoints.userProfile}${this.$route.params.id}/info/`
        );
        this.user = response.data;
        this.fetchFriendsCount();
        this.fetchUserPosts();
        if (this.activeTab === "friends") {
          this.fetchFriends();
        }
        this.fetchFriendshipStatus();
        this.fetchCurrentUser();
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
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
        const endpoint = `${endpoints.posts}?user_id=${this.user.id}&page=${this.page}`;
        console.log("Fetching posts from:", endpoint);

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
    goToFriendProfile(friendId) {
      this.$router.push({
        name: "profile",
        params: { id: friendId },
      });
    },
    async addFriend() {
      try {
        await this.fetchCurrentUser();
        const response = await axiosInstance.post(endpoints.friendRequests, {
          to_user: this.user.id,
          from_user: this.currentUser.id,
        });
        this.friendRequestSent = true;
        this.friendRequestId = response.data.id;
      } catch (error) {
        console.error("Error sending friend request:", error);
      }
    },
    async cancelFriendRequest() {
      try {
        await axiosInstance.delete(
          `${endpoints.friendRequests}${this.friendRequestId}/`
        );
        this.friendRequestSent = false;
        this.friendRequestId = null;
      } catch (error) {
        console.error("Error canceling friend request:", error);
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
  height: 80vh;
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
</style>
