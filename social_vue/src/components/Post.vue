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

      <!-- Like and Comment buttons -->
      <div class="button-wrapper">
        <!-- Thumbs up (Like) button -->
        <svg
          @click="toggleLike(post)"
          class="like-icon"
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          :fill="post.liked ? 'black' : '#e8eaed'"
        >
          <path
            d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z"
          />
        </svg>
        <!-- Comment button -->
        <svg
          @click="openComment(post)"
          class="comment-icon"
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          fill="#e8eaed"
        >
          <path
            d="M240-400h320v-80H240v80Zm0-120h480v-80H240v80Zm0-120h480v-80H240v80ZM80-80v-720q0-33 23.5-56.5T160-880h640q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H240L80-80Zm126-240h594v-480H160v525l46-45Zm-46 0v-480 480Z"
          />
        </svg>
      </div>

      <div class="border-bottom-divider"></div>

      <!-- Comment section -->
      <div class="comment-section">
        <div v-if="post.comments && post.comments.length" class="comments">
          <button class="viewMoreComments" @click="viewMoreComments(post)">
            View more comments
          </button>
          <!-- HTML -->
          <!-- HTML -->
          <!-- HTML -->
          <ul class="comments-list">
            <li
              v-for="comment in post.comments"
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

        <div class="comment-input-wrapper">
          <textarea
            v-model="post.commentText"
            class="comment-input"
            placeholder="Write a comment..."
          ></textarea>
          <!-- SVG icon for sending comment -->
          <svg
            v-if="post.commentText"
            @click="postComment(post.id, post.commentText)"
            class="send-icon"
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
            fill="#e8eaed"
          >
            <path
              d="M120-160v-640l760 320-760 320Zm80-120 474-200-474-200v140l240 60-240 60v140Zm0 0v-400 400Z"
            />
          </svg>
        </div>
      </div>
    </div>
    <comment-modal
      v-if="isModalOpen"
      :post="selectedPost"
      @close="isModalOpen = false"
    />
  </div>
</template>

<script>
import axios from "axios";
import CommentModal from "./CommentModal.vue";

export default {
  components: {
    CommentModal,
  },
  data() {
    return {
      posts: [],
      isModalOpen: false,
      selectedPost: null,
    };
  },
  mounted() {
    this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      try {
        const token = this.$store.getters.getAuthToken;
        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };

        const response = await axios.get(
          "http://127.0.0.1:8000/api/posts/friends_posts/",
          config
        );

        const posts = response.data.map(async (post) => {
          try {
            const commentsResponse = await axios.get(
              `http://127.0.0.1:8000/api/comments/?post_id=${post.id}&latest=true`,
              config
            );
            post.comments = commentsResponse.data; // Assign fetched comments to the post
          } catch (error) {
            console.error(
              `Error fetching comments for post ${post.id}:`,
              error
            );
            post.comments = []; // Default to an empty array on error
          }
          return post;
        });

        this.posts = await Promise.all(posts); // Wait for all comments to be fetched
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },

    async likePost(postId) {
      try {
        const token = this.$store.getters.getAuthToken;
        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };
        await axios.post(
          `http://127.0.0.1:8000/api/likes/?post=${postId}`, // Include postId in the URL
          {}, // No need for a request body
          config
        );
        // Update the posts to reflect the change in likes
        this.fetchPosts();
      } catch (error) {
        console.error("Error liking post:", error);
      }
    },

    async unlikePost(postId) {
      try {
        const token = this.$store.getters.getAuthToken;
        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };
        await axios.delete(
          `http://127.0.0.1:8000/api/unlike/?like=${postId}`,
          config
        );
        // Update the posts to reflect the change in likes
        this.fetchPosts();
      } catch (error) {
        console.error("Error unliking post:", error);
      }
    },

    async postComment(postId, commentText) {
      try {
        const token = this.$store.getters.getAuthToken;
        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };
        await axios.post(
          "http://127.0.0.1:8000/api/comments/",
          {
            post: postId,
            text: commentText,
          },
          config
        );
        // Clear the comment text area after posting
        this.commentText = "";
        // Update the posts to reflect the new comment
        this.fetchPosts();
      } catch (error) {
        console.error("Error posting comment:", error);
      }
    },

    async toggleLike(post) {
      try {
        console.log("toggleLike method called");
        // Determine whether to like or unlike the post based on its current state
        if (post.liked) {
          // If the post is already liked, unlike it
          await this.unlikePost(post.id);
        } else {
          // If the post is not liked, like it
          await this.likePost(post.id);
        }
      } catch (error) {
        console.error("Error toggling like:", error);
      }
    },

    viewMoreComments(post) {
      this.selectedPost = post;
      this.isModalOpen = true;
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
input[type="text"]:focus,
input[type="text"]:active,
textarea:focus,
textarea:active {
  outline: none;
}

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

.button-wrapper {
  display: flex;
  gap: 100px;
  margin-top: 5px;
  align-items: center;
  justify-content: center;
}

.like-icon:hover,
.comment-icon:hover {
  fill: lightgrey;
  cursor: pointer;
}

.comment-section {
  margin-top: 10px;
}

.comment-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
}

.comment-input {
  width: 430px;
  border: 1px solid #eff2f5;
  border-radius: 15px;
  resize: none;
  font-family: Arial, Helvetica, sans-serif;
  padding: 10px;
  background-color: #eff2f5;
}

.send-icon {
  fill: #e8eaed;
  width: 24px;
  height: 24px;
  cursor: pointer;
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
}

.send-icon:hover {
  fill: lightgrey;
}

.border-bottom-divider {
  border-bottom: 1px solid #eff2f9;
  margin-bottom: 0px;
  margin-top: 20px;
}

/* Comment Modal styles */
.viewMoreComments {
  border: none;
  background-color: transparent;
  color: black;
  font-size: 14px;
  font-weight: 400;
  text-align: start;
  cursor: pointer;
}

.viewMoreComments:hover {
  text-decoration: underline;
}

/* Comment list styles */
.comments-list {
  list-style: none;
  padding: 0;
  margin: 0;
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
