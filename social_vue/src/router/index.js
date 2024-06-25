// index.js
import { createRouter, createWebHistory } from "vue-router";
import MainLayout from "@/components/Layouts/MainLayout.vue";
import AnonLayout from "@/components/Layouts/AnonLayout.vue";
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import SignUpPage from "../views/SignUpPage/SignUpPage.vue";
import LogInPage from "../views/LogInPage/LogInPage.vue";
import ProfilePage from "../views/ProfilePage/ProfilePage.vue";
import EditProfilePage from "../views/EditProfilePage/EditProfilePage.vue";
import FriendRequestsPage from "../views/FriendRequestsPage/FriendRequestsPage.vue";

const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        name: "home",
        component: HomeView,
      },
      {
        path: "about",
        name: "about",
        component: AboutView,
      },
      {
        path: "profile/:id",
        name: "profile",
        component: ProfilePage,
        props: true,
      },
      {
        path: "/profile/:id/edit",
        name: "editProfile",
        component: EditProfilePage,
        props: true,
      },
      {
        path: "friend-requests",
        name: "friendrequests",
        component: FriendRequestsPage,
      },
    ],
  },
  {
    path: "/",
    component: AnonLayout,
    children: [
      {
        path: "signup",
        name: "signup",
        component: SignUpPage,
      },
      {
        path: "login",
        name: "login",
        component: LogInPage,
      },
    ],
  },
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
