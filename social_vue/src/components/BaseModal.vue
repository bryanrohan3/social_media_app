<template>
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <img
          src="@/assets/arrow_back.svg"
          class="back-arrow"
          @click.stop="closeModal"
          alt="Close Modal"
        />
        <div class="title-container">
          <h2 class="title"><slot name="title">Modal Title</slot></h2>
        </div>
        <button
          v-if="showAction"
          class="share-button"
          @click.stop="handleAction"
        >
          <slot name="action">Share</slot>
        </button>
      </div>
      <div class="modal-body">
        <slot> </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showModal: {
      type: Boolean,
      required: true,
    },
    showAction: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    handleAction() {
      this.$emit("action");
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

.close-button {
  background: #ccc;
  color: black;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* new */

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

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.success-message {
  display: flex;
  align-items: center;
  margin-top: 20px;
  color: green;
  font-weight: bold;
}

.success-message svg {
  margin-right: 8px;
}

@media screen and (max-width: 600px) {
  .modal-content {
    padding: 10px; /* Adjust padding for smaller screens */
  }
}
</style>
