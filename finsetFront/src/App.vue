<template>
  <div style="background-color:#e7f0f7 ;">
    <Header/>

    <header>
    
    
    <RouterLink :to="{name:'home'}"></RouterLink>
    
      
      
      
    <RouterView/>
      

      
    </header>
  </div>
</template>

<script setup>
import { RouterLink,RouterView } from 'vue-router';
import Header from "@/views/Header.vue";

 
</script>

<style  scoped>
/* global.css 또는 App.vue */
body {
  background-color: #e7f0f7; /* 모든 페이지에 배경색 적용 */
  margin: 0;
  font-family: Arial, sans-serif;
}

</style>