<template>
  <div class="signup">
    <h2>Sign up to iSocial</h2>
    <p class="welcome-message">
      Enter in the details below to set up your account
    </p>
    <form @submit.prevent="handleSignUp">
      <!-- UserName -->
      <div class="form-group">
        <label for="username"><b>Username</b></label>
        <input v-model="username" type="text" id="username" />
      </div>

      <div class="form-group">
        <label for="firstName"><b>First Name</b></label>
        <input v-model="firstName" type="text" id="firstName" required />
      </div>

      <div class="form-group">
        <label for="lastName"><b>Last Name</b></label>
        <input v-model="lastName" type="text" id="lastName" required />
      </div>

      <div class="form-group">
        <label for="email"><b>Email</b></label>
        <input v-model="email" type="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="password"><b>Password</b></label>
        <input v-model="password" type="password" id="password" required />
      </div>

      <div class="form-group">
        <label for="confirmPassword"><b>Confirm Password</b></label>
        <input
          v-model="confirmPassword"
          type="password"
          id="confirmPassword"
          required
        />
      </div>

      <button type="submit">Sign Up</button>
    </form>

    <p v-if="errorMessage">{{ errorMessage }}</p>

    <!-- "Already have an account? Log in" link -->
    <p>
      Already have an account?
      <a href="/login" class="login-link">Log in</a>
    </p>
  </div>
</template>

<script>
import axios from "axios";
import { mapMutations } from "vuex";

export default {
  data() {
    return {
      username: "",
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      confirmPassword: "",
      errorMessage: "",
    };
  },
  methods: {
    ...mapMutations(["setAuthToken", "setUserProfile"]),
    async handleSignUp() {
      // Check if passwords match
      if (this.password !== this.confirmPassword) {
        this.errorMessage = "Passwords do not match!";
        return;
      }

      try {
        // Sign up the user
        const response = await axios.post("http://localhost:8000/api/users/", {
          username: this.username,
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          password: this.password,
        });

        // Log in the user immediately after signup
        const loginResponse = await axios.post(
          "http://localhost:8000/api/users/login/",
          {
            username: this.username,
            password: this.password,
          }
        );

        // Retrieve the authentication token and user profile
        const token = loginResponse.data.token;
        const user = loginResponse.data.user;

        // Store token and user in Vuex
        this.setAuthToken(token);
        this.setUserProfile(user);

        // Redirect to home page or any desired page
        setTimeout(() => {
          this.$router.push("/");
        }, 500);
      } catch (error) {
        console.error(error.response.data);
        this.errorMessage = error.response.data.error || "An error occurred";
      }
    },
  },
};
</script>

<style>
html,
body {
  height: 100%;
  margin: 0;
  margin-bottom: 200px;
  padding: 0;
  background-color: #f9f9fd;
  background-image: radial-gradient(#e9e9e5 1.85px, transparent 1.85px),
    radial-gradient(#e9e9e5 1.85px, #f9f9fd 1.85px);
  background-size: 74px 74px;
  background-position: 0 0, 37px 37px;
}
.signup {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px; /* Add margin bottom */
}

.forgot-password-link {
  text-decoration: none;
  font-weight: bold;
  color: #27282a;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

label {
  margin-bottom: 0.25rem;
  align-self: flex-start;
}

input[type="text"],
input[type="password"],
input[type="email"] {
  width: 100%;
  padding: 0.75rem;
  box-sizing: border-box;
  border: 1px solid #ececec;
  border-radius: 10px;
}

button {
  padding: 0.85rem 1rem;
  background-color: #27282a;
  color: #fff;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  border-radius: 10px;
}

.title {
  font-family: "Pixelated MS Sans Serif", Arial;
  font-size: 32px;
  font-weight: 800;
  text-align: center;
  margin-bottom: 2rem;
}

.login-link {
  text-decoration: none;
  font-weight: bold;
  color: #27282a;
}

@media (max-width: 600px) {
  .signup {
    margin: 20px;
    padding: 1rem;
    max-width: 90%;
  }

  button {
    padding: 0.5rem;
  }
}
</style>
