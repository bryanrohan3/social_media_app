<template>
  <BaseModal :show-modal="true" @close="handleClose">
    <template v-slot:title>{{ post.username }}'s Post</template>
    <div class="modal-body">
      <div v-if="comments.length">
        <ul class="comments-list">
          <li
            v-for="comment in comments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-avatar">
              <img src="@/assets/avatar.jpeg" alt="Avatar" />
            </div>
            <div class="comment-content">
              <div class="comment-meta">
                <span class="comment-username">{{ comment.username }}</span>
                <span class="comment-date">{{
                  formatDate(comment.date_time_created)
                }}</span>
              </div>
              <p class="comment-text">{{ comment.text }}</p>
            </div>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No comments to display.</p>
      </div>
    </div>
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal.vue";
import { axiosInstance, endpoints } from "@/api/axiosHelper";
import { formatDate } from "@/api/formatDateHelpers";

export default {
  components: {
    BaseModal,
  },
  props: {
    post: {
      type: Object,
      required: true,
    },
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
        const response = await axiosInstance.get(
          `${endpoints.comments}?post_id=${this.post.id}`
        );
        this.comments = response.data;
        console.log("Fetched comments:", this.comments); // Check console for fetched comments
      } catch (error) {
        console.error(
          `Error fetching comments for post ${this.post.id}:`,
          error
        );
        this.comments = []; // Handle error by setting comments to empty array
      }
    },
    handleClose() {
      console.log("Close event received in CommentModal");
      this.$emit("close"); // Emit close event to parent
    },
    formatDate,
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
