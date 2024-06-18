<template>
  <div class="wrapper">
    <NavBar />
    <div class="content">
      <div class="centre-content">
        <h1 class="title">Friend Requests</h1>
        <div v-if="loading">Loading...</div>
        <div v-if="error">{{ error }}</div>
        <div v-if="!loading && !error">
          <details open>
            <summary class="dropdown-title">Incoming Requests</summary>
            <div
              v-for="request in receivedRequests"
              :key="request.id"
              class="friend-request"
            >
              <img
                class="profile-avatar"
                src="@/assets/avatar.jpeg"
                alt="Avatar"
              />
              <span class="username">{{ request.from_user_username }}</span>
              <button @click="handleRequest(request.id, 'accepted')">
                Confirm
              </button>
              <button @click="handleRequest(request.id, 'rejected')">
                Delete
              </button>
            </div>
          </details>

          <details open>
            <summary class="dropdown-title">Sent Requests</summary>
            <div
              v-for="request in sentRequests"
              :key="request.id"
              class="friend-request"
            >
              <img
                class="profile-avatar"
                src="@/assets/avatar.jpeg"
                alt="Avatar"
              />
              <span class="username">{{ request.to_user_username }}</span>
              <button @click="cancelRequest(request.id)">Cancel Request</button>
            </div>
          </details>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { axiosInstance, endpoints } from "@/api/axiosHelper";

export default {
  name: "FriendRequestsPage",
  components: {
    NavBar,
  },
  data() {
    return {
      receivedRequests: [],
      sentRequests: [],
      loading: true,
      error: null,
    };
  },
  methods: {
    fetchFriendRequests() {
      axiosInstance
        .get(endpoints.pendingRequests)
        .then((response) => {
          this.receivedRequests = response.data.received_requests;
          this.sentRequests = response.data.sent_requests;
          this.loading = false;
        })
        .catch((error) => {
          this.error = "Failed to load friend requests.";
          this.loading = false;
        });
    },
    handleRequest(requestId, status) {
      axiosInstance
        .patch(`${endpoints.friendRequests}${requestId}/`, {
          status: status,
        })
        .then(() => {
          this.fetchFriendRequests();
        })
        .catch(() => {
          this.error = "Failed to update friend request.";
        });
    },
    cancelRequest(requestId) {
      axiosInstance
        .delete(`${endpoints.friendRequests}${requestId}/`)
        .then(() => {
          this.fetchFriendRequests();
        })
        .catch(() => {
          this.error = "Failed to cancel friend request.";
        });
    },
  },
  mounted() {
    this.fetchFriendRequests();
  },
};
</script>

<style scoped>
.wrapper {
  display: flex;
  height: 100vh;
  position: relative;
}

.content {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto; /* Center the content */
  display: flex;
  justify-content: center; /* Center the content horizontally */
}

.title {
  font-size: 20px;
  margin-bottom: 20px;

  max-width: 200px; /* Ensure title does not exceed max width */
  min-width: 200px;
}

.friend-request {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Ensure content is evenly spaced */
  margin-bottom: 5px;
  padding: 15px;
  background-color: #fff;
  border-radius: 10px;
  transition: box-shadow 0.3s ease;
  width: 400px; /* Fixed width */
}

.profile-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
  flex-grow: 1; /* Allow username to take available space */
  text-align: start;
  font-size: 14px;
}

.friend-request button {
  min-width: 60px;
  max-width: fit-content;
  padding: 6px 10px; /* Adjust padding to make buttons smaller */
  font-size: 14px;
  cursor: pointer;
  background-color: gainsboro;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  transition: background-color 0.3s ease;
  margin-left: 10px; /* Add margin to separate buttons */
}

.centre-content {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center content horizontally */
}

.friend-request button:hover {
  background-color: #363636;
  transform: scale(1.05);
}

.dropdown-title {
  font-weight: bold;
  cursor: pointer;
  font-size: 18px;
  margin-bottom: 10px;
  text-align: left; /* Align dropdown titles to the left */
  width: 100%;
  max-width: 600px; /* Ensure dropdown titles do not exceed max width */
  padding-left: 20px; /* Move dropdown titles to the left */
}

details {
  max-width: 200px; /* Ensure details do not exceed max width */
  min-width: 200px;
  text-align: center;
  text-align: left; /* Align content inside details to the left */
  padding-left: 20px; /* Move details content to the left */
}
</style>
