import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Message from "../views/Message";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      title: "Home",
    },
  },
  {
    path: "/message",
    name: "Message",
    component: Message,
    meta: {
      title: 'message',
      
    }
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
