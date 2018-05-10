
<head>
  <title>Replace Me</title>
</head>
<template>
  <div id="app">
    <!-- <div class="limited-nav"> -->
      <el-menu mode="horizontal" @select="handleSelect" style="position: fixed; top: 0; width: 100%; margin-top: 10px; margin-right: 10px; z-index: 1234; opacity: 0.95;">
        <el-menu-item index="1" @click="toblogs()">blogs</el-menu-item>
        <el-menu-item index="2" @click="toboe()">betonether</el-menu-item>
        <el-menu-item index="3" @click="togithub()">my github</el-menu-item>
      </el-menu>
    <!-- </div> -->

    <div class="main" style="margin-top: 60px;border-radius: 10px;min-height: 620px;">
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
  },
  methods: {
    toblogs () {
      this.$router.push({ name: 'index' })
    },
    toboe () {
      this.$router.push({ name: 'betonether', params: { id: 0 } })
    },
    togithub () {
      window.location.href = 'https://github.com/guoxingx'
    }
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
  margin-top: 0px;
}
</style>
