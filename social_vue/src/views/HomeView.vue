<template>
  <div>
    <NavBar />
    <div class="content">
      <Post :posts="posts" :post-comment="postComment" />
    </div>
    <a
      href="/#"
      class="user-info-top-right"
      v-if="userProfile && userProfile.username"
    >
      <div class="comment-avatar">
        <img class="profile-avatar" src="@/assets/avatar.jpeg" alt="Avatar" />
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
import { axiosInstance, endpoints } from "@/api/axiosHelper"; // Import Axios instance

export default {
  components: {
    NavBar,
    Post,
  },
  data() {
    return {
      posts: [], // Initialize posts array
    };
  },
  computed: {
    ...mapGetters(["getUserProfile"]),
    userProfile() {
      return this.getUserProfile;
    },
  },
  mounted() {
    this.fetchPosts(); // Fetch posts when the component is mounted
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axiosInstance.get(endpoints.posts);

        const posts = response.data.map(async (post) => {
          try {
            const commentsResponse = await axiosInstance.get(
              `${endpoints.comments}?post_id=${post.id}&latest=true`
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
        await axiosInstance.post(`${endpoints.likes}?post=${postId}`);
        // Update the posts to reflect the change in likes
        this.fetchPosts();
      } catch (error) {
        console.error("Error liking post:", error);
      }
    },

    async unlikePost(postId) {
      try {
        await axiosInstance.delete(`${endpoints.likes}?like=${postId}`);
        // Update the posts to reflect the change in likes
        this.fetchPosts();
      } catch (error) {
        console.error("Error unliking post:", error);
      }
    },

    async postComment(postId, commentText) {
      try {
        await axiosInstance.post(endpoints.comments, {
          post: postId,
          text: commentText,
        });
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
  },
};
</script>

<style>
.content {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto; /* Center the content */
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
  font-size: 14px;
}

.name {
  font-size: 0.9em;
  font-size: 14px;
}

.profile-avatar {
  border: 2px solid #b2b2b2;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

@media screen and (max-width: 768px) {
  .user-info-top-right {
    font-size: 0.8em;
  }
}
</style>
