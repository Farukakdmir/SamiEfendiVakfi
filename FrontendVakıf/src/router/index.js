import { createRouter, createWebHistory } from "vue-router";
import { h } from "vue";
import Login from "../views/Login.vue"; // Giriş sayfası
import Home from "../views/Home.vue"; // Ana sayfa
import Files from "../views/Files.vue"; // Dosya yönetimi sayfası
import MaddiYardim from "../views/MaddiYardim.vue";
import SahsiYardim from "../views/SahsiYardim.vue";
import DosyaDetay from "../views/DosyaDetay.vue";

// Wrapper component for MaddiYardim
const MaddiYardimWrapper = {
  name: "MaddiYardimWrapper",
  setup() {
    return () => h(MaddiYardim);
  },
};

const routes = [
  {
    path: "/",
    redirect: "/login", // Ana sayfa giriş sayfasına yönlendirir
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: { requiresGuest: true }, // Giriş yapmamış kullanıcılar için
  },
  {
    path: "/home",
    name: "home",
    component: Home,
    meta: { requiresAuth: true }, // Giriş yapmış kullanıcılar için
  },
  {
    path: "/files",
    name: "files",
    component: Files,
    meta: { requiresAuth: true }, // Giriş yapmış kullanıcılar için
  },
  {
    path: "/maddi-yardim",
    name: "maddi-yardim",
    component: MaddiYardim,
    meta: { requiresAuth: true },
  },
  {
    path: "/sahsi-yardim",
    name: "sahsi-yardim",
    component: SahsiYardim,
    meta: { requiresAuth: true },
  },
  {
    path: "/dosya/:dosyaNo",
    name: "DosyaDetay",
    component: DosyaDetay,
    props: true,
  },
  // 404 sayfası için
  {
    path: "/:pathMatch(.*)*",
    redirect: "/home", // Bulunamayan sayfalar ana sayfaya yönlendirir
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Kullanıcı kimlik doğrulaması kontrolü
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("token");

  if (to.path === "/login" && isAuthenticated) {
    next("/files");
  } else if (to.path !== "/login" && !isAuthenticated) {
    next("/login");
  } else {
    next();
  }
});

export default router;
