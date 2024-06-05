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
        <img src="" alt="Avatar" />
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
import axiosInstance from "@/api/axiosHelper"; // Import Axios instance

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
        const response = await axiosInstance.get(
          "http://127.0.0.1:8000/api/posts/friends_posts/"
        );

        const posts = response.data.map(async (post) => {
          try {
            const commentsResponse = await axiosInstance.get(
              `http://127.0.0.1:8000/api/comments/?post_id=${post.id}&latest=true`
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
        await axiosInstance.post(
          `http://127.0.0.1:8000/api/likes/?post=${postId}`, // Include postId in the URL
          {} // No need for a request body
        );
        // Update the posts to reflect the change in likes
        this.fetchPosts();
      } catch (error) {
        console.error("Error liking post:", error);
      }
    },

    async unlikePost(postId) {
      try {
        await axiosInstance.delete(
          `http://127.0.0.1:8000/api/unlike/?like=${postId}`
        );
        // Update the posts to reflect the change in likes
        this.fetchPosts();
      } catch (error) {
        console.error("Error unliking post:", error);
      }
    },

    async postComment(postId, commentText) {
      try {
        await axiosInstance.post("http://127.0.0.1:8000/api/comments/", {
          post: postId,
          text: commentText,
        });
        // Clear the comment text area after posting
        this.commentText = "";
        // Update the posts to reflect the new comment
        this.fetchPosts();
        // this.postComment(postId, commentText);
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
