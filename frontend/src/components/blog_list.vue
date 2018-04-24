<template>
  <el-row>
    <el-col :xs="2" :sm="3" :md="4" :lg="5" :xl="6">
      <div class="space left"></div>
    </el-col>
    <el-col :xs="20" :sm="18" :md="14" :lg="14" :xl="12">
      <div class="articles">
        <blog-cell v-for="article in articles" :key="article" :unit="article"></blog-cell>
      </div>
    </el-col>
    <el-col :xs="2" :sm="3" :md="4" :lg="5" :xl="6">
      <div class="space right"></div>
    </el-col>
  </el-row>
</template>

<script>
import { getArticleList } from '../requests'

export default {
  name: 'blog_list',
  components: {
    'blog-cell': () => import('./blog_cell.vue')
  },
  data () {
    return {
      articles: []
    }
  },
  created () {
    getArticleList().then(res => {
      this.articles = res.data
    })
  }
}
</script>

<style>
.articles {
  text-align: center;
}
</style>
