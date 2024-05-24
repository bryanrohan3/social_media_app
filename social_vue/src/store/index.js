import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    authToken: null,
    userProfile: null,
    expenses: [],
  },
  getters: {
    getAuthToken(state) {
      return state.authToken;
    },
    getUserProfile(state) {
      return state.userProfile;
    },
  },
  mutations: {
    setAuthToken(state, token) {
      state.authToken = token;
    },
    setUserProfile(state, user) {
      state.userProfile = user;
    },
    logout(state) {
      state.authToken = null;
      state.userProfile = null;
    },
  },
  actions: {},
  plugins: [createPersistedState()],
});
