
<head>
  <title>Replace Me</title>
</head>
<template>
  <div id="app">
    <!-- <div class="limited-nav"> -->
      <el-menu class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1" @click="toblogs()">blogs</el-menu-item>
        <el-menu-item index="2" @click="toboe()">betonether</el-menu-item>
        <el-menu-item index="3" @click="togithub()">my github</el-menu-item>
      </el-menu>
    <!-- </div> -->

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
.main {
  border-radius: 10px;
  min-height: 620px;
}
.space {
  min-height: 100px;
}
.limited-nav {
  /*width: 200px;*/
  min-width: 200px;
  max-width: 760px;
  margin: 0 auto;
}
</style>
