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
import { axiosInstance, endpoints } from "@/api/axiosHelper";

export default {
  components: {
    NavBar,
    Post,
  },
  data() {
    return {
      posts: [],
    };
  },
  computed: {
    ...mapGetters(["getUserProfile"]),
    userProfile() {
      return this.getUserProfile;
    },
  },
  mounted() {
    this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axiosInstance.get(
          endpoints.posts + "friends_posts/"
        );

        // Directly use the response data without additional API calls for comments
        const posts = response.data.map((post) => {
          if (post.latest_comment) {
            post.comments = [post.latest_comment]; // Assign the latest comment to the post's comments
          } else {
            post.comments = []; // Default to an empty array if no latest comment is present
          }
          return post;
        });

        this.posts = posts; // No need to use Promise.all since we're not dealing with async operations within the map
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },

    async likePost(postId) {
      try {
        await axiosInstance.post(`${endpoints.likes}?post=${postId}`);
        this.fetchPosts();
      } catch (error) {
        console.error("Error liking post:", error);
      }
    },

    async unlikePost(postId) {
      try {
        await axiosInstance.delete(`${endpoints.likes}?like=${postId}`);
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
        this.fetchPosts();
      } catch (error) {
        console.error("Error posting comment:", error);
      }
    },

    async viewMoreComments(post) {
      // Implement the logic here to show more comments for the post
      console.log("View more comments for post:", post);
      // Example: You might want to expand a modal or toggle a state
    },

    async toggleLike(post) {
      try {
        if (post.liked) {
          await this.unlikePost(post.id);
        } else {
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
