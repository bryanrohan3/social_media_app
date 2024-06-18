<template>
  <div class="edit-profile-wrapper">
    <NavBar />
    <div class="content">
      <h2 class="title">Edit Profile</h2>
      <div v-if="userLoaded">
        <div class="user-info">
          <div class="avatar-wrapper">
            <img class="avatar" src="@/assets/avatar.jpeg" alt="Avatar" />
          </div>
          <div class="user-details">
            <p class="username">@{{ originalUser.username }}</p>
            <p class="name">
              {{ originalUser.first_name }} {{ originalUser.last_name }}
            </p>
          </div>
        </div>
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label class="username" for="username">Username</label>
            <input
              type="text"
              v-model="user.username"
              id="username"
              required
              @input="checkChanges"
            />
          </div>
          <div class="form-group">
            <label class="username" for="first_name">First Name</label>
            <input
              type="text"
              v-model="user.first_name"
              id="first_name"
              required
              @input="checkChanges"
            />
          </div>
          <div class="form-group">
            <label class="username" for="last_name">Last Name</label>
            <input
              type="text"
              v-model="user.last_name"
              id="last_name"
              required
              @input="checkChanges"
            />
          </div>
          <button
            type="submit"
            :disabled="!isModified"
            :class="{ disabled: !isModified }"
          >
            Save Changes
          </button>
        </form>
      </div>
      <div v-else>Loading...</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import NavBar from "@/components/NavBar.vue";
import { axiosInstance, endpoints } from "@/api/axiosHelper"; // Import Axios instance

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      user: null,
      originalUser: null,
      userLoaded: false,
      isModified: false,
    };
  },
  computed: {
    ...mapGetters(["getAuthToken"]),
  },
  mounted() {
    this.fetchCurrentUser();
  },
  methods: {
    async fetchCurrentUser() {
      try {
        const response = await axiosInstance.get(endpoints.currentUser);
        this.user = { ...response.data };
        this.originalUser = { ...response.data };
        this.userLoaded = true;
      } catch (error) {
        console.error("Error fetching current user data:", error);
      }
    },
    checkChanges() {
      this.isModified =
        this.user.username !== this.originalUser.username ||
        this.user.first_name !== this.originalUser.first_name ||
        this.user.last_name !== this.originalUser.last_name;
    },
    async updateProfile() {
      try {
        if (this.isModified) {
          const updatedUser = {
            username: this.user.username,
            first_name: this.user.first_name,
            last_name: this.user.last_name,
          };
          await axiosInstance.patch(
            `${endpoints.updateUser}${this.user.id}/`,
            updatedUser
          );
          this.$router.push("/myprofile");
        }
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    },
  },
};
</script>

<style scoped>
.edit-profile-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 20px;
}

.content {
  width: 400px;
  max-width: 600px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  width: 100px;
  margin-bottom: 5px;
}

input {
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 10px;
  outline: #fff;
}

button {
  padding: 10px 20px;
  background-color: #363636;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: calc(100% - 20px); /* Adjust button width */
}

button.disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(.disabled) {
  background-color: #1e1e1e;
}

.title {
  font-size: 20px;
  margin-left: auto; /* This will align the title with the right edge */
  font-weight: bold;
  margin-bottom: 20px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.username {
  font-weight: bold;
  padding-left: 0;
  margin: 0;
}

.name {
  padding-left: 0;
  margin: 8px 0;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  padding: 15px;
  background-color: #efefef;
  border-radius: 30px;
}

.avatar-wrapper {
  margin-right: 30px;
  margin-left: 10px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.user-details {
  margin: 0;
}
</style>
