<!-- src/App.vue -->
<template>
  <Header />
  <router-view />   <!-- ここに各ページがレンダリングされる -->
</template>

<script setup>
import Header from './components/shared/Header.vue'
import './assets/css/main.css'
import { onMounted } from 'vue'
onMounted(() => {
  console.log('App mounted!')
})


</script>

<style>
body {
  padding:0;
  margin:0;
  width: 100%;
  
}
#app {
  display: flex;
  flex-direction: column; /* ←縦に積む */
  padding:0;
  margin:0;
  width: 100%;
}

/* もし body に flex が当たっている場合はリセット */
body {
  display: block; /* もしくは flex-direction:column; */
}
</style>