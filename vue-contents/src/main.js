// vue-contents/src/main.js
import { createApp } from 'vue'
import App from './App.vue'           // ルートはApp.vueにする
import router from './router'         // ルーターをインポート
import axios from 'axios'
import './assets/css/main.css'

axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const app = createApp(App)            // App.vueをベースにアプリ生成
app.use(router)                       // ルーターを有効化
app.mount('#app')                     // マウント
