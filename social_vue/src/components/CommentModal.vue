<!-- CommentModal.vue -->
<template>
  <div class="modal">
    <div class="modal-content">
      <span class="close" @click="$emit('close')">&times;</span>
      <h2>{{ post.username }}'s Post</h2>
      <div v-if="comments.length">
        <ul class="comments-list">
          <li
            v-for="comment in comments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-avatar">
              <img src="https://via.placeholder.com/40" alt="Avatar" />
            </div>
            <div class="comment-content">
              <div class="comment-meta">
                <span class="comment-username">{{ comment.username }}</span>
              </div>
              <p class="comment-text">{{ comment.text }}</p>
              <span class="comment-date">{{
                formatDate(comment.date_time_created)
              }}</span>
            </div>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No comments to display.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    post: Object,
  },
  data() {
    return {
      comments: [],
    };
  },
  mounted() {
    this.fetchAllComments();
  },
  methods: {
    async fetchAllComments() {
      try {
        const token = this.$store.getters.getAuthToken;
        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };

        const response = await axios.get(
          `http://127.0.0.1:8000/api/comments/?post_id=${this.post.id}`,
          config
        );

        this.comments = response.data;
      } catch (error) {
        console.error(
          `Error fetching all comments for post ${this.post.id}:`,
          error
        );
        this.comments = [];
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
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 600px;
  border-radius: 10px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

/* Comment list styles */
.comments-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  max-height: 500px;
}

.comment-item {
  display: flex;
  align-items: flex-start;
  padding: 10px 0;
  margin-bottom: 5px;
}

.comment-avatar {
  margin-right: 10px;
}

.comment-avatar img {
  border-radius: 50%;
  width: 30px;
  height: 30px;
}

.comment-content {
  flex: 1;
  background-color: #f0f2f5;
  padding: 10px;
  border-radius: 12px;
}

.comment-text {
  margin: 0;
  color: #1c1e21;
  text-align: start;
}

.comment-meta {
  display: flex;
  gap: 10px;
  font-size: 0.975rem;
  align-items: flex-end;
}

.comment-username {
  font-weight: bold;
}

.comment-date {
  color: #65676b;
  font-size: 0.725rem;
  margin-top: 5px;
  display: flex;
}
</style>