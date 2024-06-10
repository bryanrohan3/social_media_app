<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <svg
          class="back-arrow"
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          fill="#000000"
          @click="closeModal"
        >
          <path
            d="m313-440 224 224-57 56-320-320 320-320 57 56-224 224h487v80H313Z"
          />
        </svg>
        <div class="title-container">
          <h2 class="title">Create new post</h2>
        </div>
        <button class="share-button" @click="createPost">Share</button>
      </div>

      <div class="user-info">
        <img class="user-picture" src="@/assets/avatar.jpeg" alt="Avatar" />
        <span class="username">{{ userProfile.username }}</span>
      </div>

      <form @submit.prevent="createPost">
        <div class="form-group">
          <textarea
            v-model="caption"
            id="caption"
            placeholder="Write a caption..."
            maxlength="2200"
            required
          ></textarea>
        </div>
        <div class="form-footer">
          <span class="emoji-icon"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              height="24px"
              viewBox="0 -960 960 960"
              width="24px"
              fill="#000000"
            >
              <path
                d="M480-480Zm0 400q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q43 0 83 8.5t77 24.5v90q-35-20-75.5-31.5T480-800q-133 0-226.5 93.5T160-480q0 133 93.5 226.5T480-160q133 0 226.5-93.5T800-480q0-32-6.5-62T776-600h86q9 29 13.5 58.5T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm320-600v-80h-80v-80h80v-80h80v80h80v80h-80v80h-80ZM620-520q25 0 42.5-17.5T680-580q0-25-17.5-42.5T620-640q-25 0-42.5 17.5T560-580q0 25 17.5 42.5T620-520Zm-280 0q25 0 42.5-17.5T400-580q0-25-17.5-42.5T340-640q-25 0-42.5 17.5T280-580q0 25 17.5 42.5T340-520Zm140 260q68 0 123.5-38.5T684-400H276q25 63 80.5 101.5T480-260Z"
              /></svg
          ></span>
          <span class="char-counter">{{ caption.length }}/2,200</span>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"; // Import mapGetters from Vuex
import axiosInstance from "@/api/axiosHelper";

export default {
  data() {
    return {
      caption: "",
    };
  },
  computed: {
    ...mapGetters(["getUserProfile"]), // Map the getUserProfile getter
    userProfile() {
      return this.getUserProfile;
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    async createPost() {
      try {
        const response = await axiosInstance.post(
          "http://127.0.0.1:8000/api/posts/",
          {
            caption: this.caption,
          }
        );
        console.log("Post created:", response.data);
        this.closeModal();
      } catch (error) {
        console.error("Error creating post:", error);
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure the modal overlay is on top */
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1001; /* Ensure the modal content is on top of the overlay */
}

.modal-header {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 20px;
  padding-top: 5px;
}

.back-arrow {
  position: absolute;
  left: 0;
  cursor: pointer;
}

.title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  margin-right: 60px; /* Adjust this value as needed */
}

.share-button {
  position: absolute;
  margin-left: 280px;
  background: none;
  border: none;
  color: #3897f0;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  margin: 20px 0;
}

.user-picture {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  border: 2px solid lightgray;
}

.username {
  font-weight: bold;
}

.form-group {
  margin-bottom: 15px;
}

textarea {
  width: 100%;
  height: 200px;
  border: none;
  outline: none;
  resize: none;
  font-size: 14px;
  padding: 10px;
  border-radius: 8px;
  background: #f9f9f9;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.emoji-icon {
  font-size: 24px;
  cursor: pointer;
}

.char-counter {
  font-size: 12px;
  color: #999;
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #ddd;
  padding-bottom: 20px;
  padding-top: 5px;
  position: relative;
}

.back-arrow {
  cursor: pointer;
}

.title-container {
  flex-grow: 1;
  display: flex;
  align-items: center; /* Updated: Align items vertically center */
  justify-content: center;
}

.title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}

.share-button {
  background: none;
  border: none;
  color: #3897f0;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
}

@media screen and (max-width: 600px) {
  .modal-content {
    padding: 10px; /* Adjust padding for smaller screens */
  }
}
</style>
