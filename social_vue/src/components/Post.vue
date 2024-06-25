<template>
  <div class="post-container">
    <div v-for="post in sortedPosts" :key="post.id" class="post">
      <div class="post-header">
        <img class="avatar" src="../assets/avatar.jpeg" alt="Avatar" />
        <div class="user-info">
          <p class="username">{{ post.username }}</p>
          <p class="date">{{ formatDate(post.date_time_created) }}</p>
        </div>
      </div>
      <p class="caption">{{ post.caption }}</p>
      <div class="button-wrapper">
        <svg
          @click="toggleLike(post)"
          class="like-icon"
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          :fill="post.liked ? 'orange' : 'gray'"
        >
          <path
            d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z"
          />
        </svg>
        <svg
          @click="openComment(post)"
          class="comment-icon"
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          fill="gray"
        >
          <path
            d="M240-400h320v-80H240v80Zm0-120h480v-80H240v80Zm0-120h480v-80H240v80ZM80-80v-720q0-33 23.5-56.5T160-880h640q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H240L80-80Zm126-240h594v-480H160v525l46-45Zm-46 0v-480 480Z"
          />
        </svg>
      </div>

      <div class="border-bottom-divider"></div>

      <div class="comment-section">
        <div v-if="post.comments && post.comments.length > 0" class="comments">
          <button class="viewMoreComments" @click="viewMoreComments(post)">
            View more comments
          </button>

          <ul class="comments-list">
            <li
              v-for="comment in post.comments"
              :key="comment.id"
              class="comment-item"
            >
              <div class="comment-avatar">
                <img src="../assets/avatar.jpeg" alt="Avatar" />
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
            :id="'comment-input-' + post.id"
          ></textarea>
          <svg
            v-if="post.commentText"
            @click="postComment(post.id, post.commentText)"
            class="send-icon"
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
            fill="gray"
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
import CommentModal from "./CommentModal.vue";
import { mapGetters } from "vuex";
import { axiosInstance, endpoints } from "@/api/axiosHelper"; // Import Axios instance and endpoints
import { formatDate } from "@/api/formatDateHelpers"; // Import the formatDate function

export default {
  components: {
    CommentModal,
  },
  computed: {
    ...mapGetters(["getAuthToken"]),
    sortedPosts() {
      // Return posts as they are received from the backend
      return this.posts || [];
    },
  },

  created() {
    this.postsData = this.sortPosts(this.posts);
  },
  props: {
    posts: {
      type: Array,
      default: () => [],
    },
    postComment: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      postsData: [],
      isModalOpen: false,
      selectedPost: null,
    };
  },
  methods: {
    viewMoreComments(post) {
      this.selectedPost = post;
      this.isModalOpen = true;
    },
    formatDate,
    sortPosts(posts) {
      return posts
        .slice()
        .sort(
          (a, b) =>
            new Date(b.date_time_created) - new Date(a.date_time_created)
        );
    },
    openComment(post) {
      // Set the selected post
      this.selectedPost = post;
      // Get the comment input field of the specific post
      const commentInput = document.getElementById(`comment-input-${post.id}`);
      if (commentInput) {
        // Calculate the position of the comment input field relative to the viewport
        const rect = commentInput.getBoundingClientRect();
        // Scroll to the comment input field, keeping the post in view
        window.scrollTo({
          top: window.pageYOffset + rect.top - 200, // Adjust the offset as needed
          behavior: "smooth",
        });
        // Focus on the comment input field
        commentInput.focus();
      }
    },

    async toggleLike(post) {
      if (post.liked) {
        // Unlike the post
        try {
          if (post.like_id) {
            await axiosInstance.delete(`${endpoints.unlike}${post.like_id}`);
            post.liked = false;
            post.like_id = null;
          } else {
            console.error("Like ID is missing");
          }
        } catch (error) {
          console.error("Error unliking the post:", error);
        }
      } else {
        // Like the post
        try {
          const response = await axiosInstance.post(endpoints.likes, {
            post: post.id,
          });
          post.liked = true;
          post.like_id = response.data.id; // Ensure this matches the backend response structure
        } catch (error) {
          console.error("Error liking the post:", error);
        }
      }
    },
  },
};
</script>

<style scoped>
.post-header {
  display: flex;
  align-items: center; /* Center items horizontally */
  gap: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #b2b2b2;
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
  transform: scale(1.1) rotate(-45deg); /* Rotate 45 degrees when clicked */
}

.like-icon,
.comment-icon {
  transition: transform 0.2s ease-in-out; /* Add a transition for the transform property */
  cursor: pointer;
}
.like-icon,
.comment-icon {
  transition: transform 0.2s ease-in-out; /* Add a transition for the transform property */
  cursor: pointer;
}

.like-icon:hover,
.comment-icon:hover,
.like-icon.clicked,
.comment-icon.clicked {
  fill: lightgrey;
  cursor: pointer;
  transform: scale(1.1); /* Scale the icon slightly when hovered or clicked */
  transform: scale(1.1) rotate(-15deg); /* Rotate 45 degrees when clicked */
}

.like-icon.clicked,
.comment-icon.clicked {
  transform: scale(1.1) rotate(45deg); /* Rotate 45 degrees when clicked */
}

.comment-section {
  margin-top: 10px;
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
  fill: gray;
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
  margin-left: 100px;
  z-index: 1; /* Ensure the post container is below the modal */
}

.post {
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.07);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  width: 450px;
  z-index: 1; /* Ensure the post is below the modal */
}

.comment-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 1; /* Ensure the comment input is below the modal */
}
</style>
