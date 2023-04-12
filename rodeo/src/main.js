import Vue from "vue";
import Vue2Editor from "vue2-editor";
import App from "./App.vue";
import router from "./router";
import store from "./store";


Vue.use(Vue2Editor);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
