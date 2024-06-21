<template>
  <div>
    <NavBar />
    <div class="content" @scroll="handleScroll">
      <Post
        :posts="posts"
        :post-comment="postComment"
        :toggle-like="toggleLike"
        :view-more-comments="viewMoreComments"
      />
      <div v-if="loading" class="loading">Loading...</div>
      <div v-if="!hasMore" class="end-of-feed">Bottom of feed</div>
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
      loading: false,
      page: 1,
      hasMore: true,
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
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    async fetchPosts() {
      if (this.loading || !this.hasMore) return;
      this.loading = true;

      try {
        const response = await axiosInstance.get(
          `${endpoints.posts}friends_posts/?page=${this.page}`
        );

        const newPosts = response.data.results;

        if (newPosts.length === 0 || response.data.next === null) {
          this.hasMore = false;
        }

        this.posts = [...this.posts, ...newPosts];
        this.page++;
      } catch (error) {
        console.error("Error fetching posts:", error);
      } finally {
        this.loading = false;
      }
    },
    handleScroll() {
      if (this.loading || !this.hasMore) return;

      const scrollHeight = document.documentElement.scrollHeight;
      const scrollTop = document.documentElement.scrollTop;
      const clientHeight = window.innerHeight;

      if (scrollTop + clientHeight >= scrollHeight - 5) {
        this.fetchPosts();
      }
    },
    async likePost(postId) {
      try {
        await axiosInstance.post(`${endpoints.likes}?post=${postId}`);
        this.updatePostLike(postId, true);
      } catch (error) {
        console.error("Error liking post:", error);
      }
    },
    async unlikePost(postId) {
      try {
        await axiosInstance.delete(`${endpoints.likes}?like=${postId}`);
        this.updatePostLike(postId, false);
      } catch (error) {
        console.error("Error unliking post:", error);
      }
    },
    updatePostLike(postId, liked) {
      const updatedPosts = this.posts.map((post) => {
        if (post.id === postId) {
          post.liked = liked;
          post.like_count += liked ? 1 : -1;
        }
        return post;
      });
      this.posts = updatedPosts;
    },
    async postComment(postId, commentText) {
      try {
        const response = await axiosInstance.post(endpoints.comments, {
          post: postId,
          text: commentText,
        });

        const newComment = response.data;
        newComment.date_time_created = new Date(newComment.date_time_created);

        const updatedPosts = this.posts.map((post) => {
          if (post.id === postId) {
            post.comments.unshift(newComment);
          }
          return post;
        });

        this.posts = updatedPosts;
      } catch (error) {
        console.error("Error posting comment:", error);
      }
    },
    async viewMoreComments(post) {
      console.log("View more comments for post:", post);
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
  height: 80vh;
}

.end-of-feed {
  padding: 40px;
  font-size: 16px;
  font-weight: 600;
  color: #b2b2b2;
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
