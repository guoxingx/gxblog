
<template>
  <div id="app">
    <div class="main">
      <!-- <keep-alive> -->
        <router-view/>
      <!-- </keep-alive> -->
    </div>
    <!-- <gFooter></gFooter> -->
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
    'gFooter': () => import('./components/footer.vue')
  }
}
</script>

<style>
body {
  background: #f9f9f9;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 50px;
}
.main {
  border-radius: 10px;
  min-height: 620px;
}
.space {
  min-height: 100px;
}
</style>
