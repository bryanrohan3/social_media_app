<template>
  <div>
    <NavBar />
    <div class="content">
      <Post />
      <h1 v-if="userProfile && userProfile.first_name">
        Hello {{ userProfile.first_name }} Hello {{ userProfile.username }}
      </h1>
      <p v-else>Please log in to see your account name.</p>
    </div>
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

h1 {
  font-family: "Arial", sans-serif;
  font-size: 2rem;
  color: #333;
}
</style>
