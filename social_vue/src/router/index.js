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
  // MyProfilePage
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
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
