import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
// Bootstrap js
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
// Bootstrap Css
import 'bootstrap/dist/css/bootstrap.min.css';
// Bootstrap icons
import '../node_modules/bootstrap-icons/font/bootstrap-icons.min.css';

const app = createApp(App)

export const pinia = createPinia();

app.use(router)

app.use(pinia);

app.mount('#app')
