import { createApp } from "vue";
import { createPinia, getActivePinia } from "pinia";
import { createVuetify } from "vuetify";
import persistedState from 'pinia-plugin-persistedstate'
import 'vuetify/styles' // Vuetify 기본 스타일
import '@mdi/font/css/materialdesignicons.css' // MDI 아이콘 스타일

// import { QuillEditor } from "@vueup/vue-quill";
// import "@vueup/vue-quill/dist/vue-quill.snow.css";

import * as components from "vuetify/components";
import * as directives from "vuetify/directives";


import App from "@/App.vue";
import router from "@/router";
// import "@/assets/index.css";

const app = createApp(App);

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi', // 기본 아이콘 세트를 MDI로 설정
  },
});

// app.component("QuillEditor", QuillEditor);

const pinia = createPinia()
pinia.use(persistedState)

app.use(pinia)
app.use(router);
app.use(vuetify);
app.mount("#app");