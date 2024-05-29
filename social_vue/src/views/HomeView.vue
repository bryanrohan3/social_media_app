<template>
  <div>
    <NavBar />
    <div class="content">
      <Post />
    </div>
    <a
      href="/#"
      class="user-info-top-right"
      v-if="userProfile && userProfile.username"
    >
      <div class="comment-avatar">
        <img src="https://via.placeholder.com/40" alt="Avatar" />
      </div>
      <div class="user-details">
        <div class="username">{{ userProfile.username }}</div>
        <div class="name">
          {{ userProfile.first_name }} {{ userProfile.last_name }}
        </div>
      </div>
    </a>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import NavBar from "@/components/NavBar.vue";
import Post from "@/components/Post.vue";

export default {
  components: {
    NavBar,
    Post,
  },
  computed: {
    ...mapGetters(["getUserProfile"]),
    userProfile() {
      return this.getUserProfile;
    },
  },
};
</script>

<style>
.content {
  flex: 1;
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 2rem;
  margin-left: 200px; /* Make space for fixed navbar */
}

.user-info-top-right {
  position: fixed;
  top: 40px; /* Adjusted */
  right: 40px; /* Adjusted */
  display: flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 5px;
  z-index: 599; /* Ensure it's above other elements */
  text-decoration: none;
  color: #333;
  font-size: 1em;
}

.comment-avatar img {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.user-details {
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-bottom: 10px;
}

.username {
  font-weight: bold;
}

.name {
  font-size: 0.9em;
}

@media screen and (max-width: 768px) {
  .user-info-top-right {
    font-size: 0.8em;
  }
}
</style>
