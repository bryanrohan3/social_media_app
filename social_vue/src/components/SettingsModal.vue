<template>
  <BaseModal :show-modal="showModal" @close="handleClose">
    <template v-slot:title>Settings</template>
    <div class="modal-body">
      <button @click="deleteAccount" class="delete-account-button">
        Delete Account
      </button>
    </div>
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal.vue";

export default {
  components: {
    BaseModal,
  },
  props: {
    showModal: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    deleteAccount() {
      // Mock function for deleting account
      alert("Account deleted");
      this.handleClose(); // Close the modal after action
    },
    handleClose() {
      console.log("Close event received in SettingsModal");
      this.$emit("update:showModal", false); // Set showModal to false
    },
  },
};
</script>

<style scoped>
.delete-account-button {
  background: #ff4d4d;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
}
</style>
