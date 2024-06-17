import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../views/AboutView.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../views/SignUpPage/SignUpPage.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LogInPage/LogInPage.vue"),
  },
  {
    path: "/myprofile",
    name: "myprofile",
    component: () => import("../views/MyProfilePage/MyProfilePage.vue"),
  },
  {
    path: "/profile/:id",
    name: "profile",
    component: () => import("../views/ProfilePage/ProfilePage.vue"),
    props: true,
  },
  {
    path: "/myprofile/edit",
    name: "editprofile",
    component: () => import("../views/EditProfilePage/EditProfilePage.vue"),
  },
  {
    path: "/friend-requests",
    name: "friendrequests",
    component: () =>
      import("../views/FriendRequestsPage/FriendRequestsPage.vue"),
  },
  // Catch-all route for undefined routes
  {
    path: "/:catchAll(.*)",
    redirect: { name: "home" },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
