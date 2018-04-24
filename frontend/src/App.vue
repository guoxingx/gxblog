<template>
  <div id="app">

    <el-row>

      <el-col :xs="3" :sm="4" :md="5" :lg="5" :xl="6">
        <div class="space left"></div>
      </el-col>

      <el-col :xs="18" :sm="16" :md="14" :lg="14" :xl="12">
        <div class="main">
          <!-- <img src="./assets/logo.png"> -->
          <router-view/>
        </div>
      </el-col>

      <el-col :xs="3" :sm="4" :md="5" :lg="5" :xl="6">
        <div class="space right"></div>
      </el-col>

    </el-row>

    <gFooter></gFooter>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
    'gFooter': () => import('./components/footer.vue')
    // 'wDialog': () => import('./components/dialog.vue')
  }
}
</script>

<style>
body {
    background: #efeff4;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 50px;
}
.main {
  background: white;
  border-radius: 10px;
  min-height: 620px;
}
.space {
  /*background: red;*/
  min-height: 100px;
}
</style>
