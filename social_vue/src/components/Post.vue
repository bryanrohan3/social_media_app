<template>
  <div class="post-container">
    <div v-for="post in posts" :key="post.id" class="post">
      <div class="post-header">
        <img class="avatar" src="https://via.placeholder.com/50" alt="Avatar" />
        <div class="user-info">
          <p class="username">{{ post.username }}</p>
          <p class="date">{{ formatDate(post.date_time_created) }}</p>
        </div>
      </div>
      <p class="caption">{{ post.caption }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      posts: [],
    };
  },
  mounted() {
    this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/posts/friends_posts/",
          {
            headers: {
              Authorization: `Token ${this.$store.getters.getAuthToken}`,
            },
          }
        );
        this.posts = response.data;
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
    formatDate(date) {
      const options = {
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      };
      const formattedDate = new Date(date);
      const year = formattedDate.getFullYear();

      if (year === 2024) {
        return (
          formattedDate.toLocaleString("en-US", {
            month: "short",
            day: "numeric",
          }) +
          " at " +
          formattedDate.toLocaleString("en-US", {
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
          })
        );
      } else {
        return (
          formattedDate.toLocaleString("en-US", {
            month: "long",
            day: "numeric",
            year: "numeric",
          }) +
          " at " +
          formattedDate.toLocaleString("en-US", {
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
          })
        );
      }
    },
  },
};
</script>

<style scoped>
.post-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-left: 200px;
}

.post {
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 20px;
  display: flex; /* Ensure the post content is flex */
  flex-direction: column; /* Arrange the content vertically */
  width: 450px;
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

  align-self: flex-start;
}

.date {
  color: #555;
  font-size: 0.8rem;
  margin: 0;
}

.caption {
  margin-top: 20px;
  align-self: flex-start;
}
</style>
