<template>
  <div>
    <el-row>
      <el-col :xs="2" :sm="2" :md="2" :lg="3" :xl="4">
        <div class="space left"></div>
      </el-col>
      <el-col :xs="20" :sm="19" :md="17" :lg="14" :xl="12">
        <div class="blogs">
          <blog-cell v-for="blog in blogs" :key="blog" :unit="blog"></blog-cell>
        </div>
      </el-col>
      <el-col :xs="2" :sm="3" :md="5" :lg="7" :xl="8">
        <div class="space right"></div>
      </el-col>
    </el-row>
    <div class="comments"></div>
  </div>
</template>

<script>
import { getBlogList } from '../requests'
import 'gitment/style/default.css'
import Gitment from 'gitment'

const gitment = new Gitment({
  // id: '',
  owner: 'guoxingx',
  repo: 'blog-comments',
  oauth: {
    client_id: 'ec6b689bac37f67820ac',
    client_secret: '6be0eaffa76662428d856119183977b652de9564'
  }
})
gitment.render('comments')

export default {
  name: 'blog_list',
  components: {
    'blog-cell': () => import('./blog_cell.vue')
  },
  data () {
    return {
      blogs: []
    }
  },
  created () {
    getBlogList().then(res => {
      this.blogs = res.data
    })
  }
}
</script>

<style>
.blogs {
  text-align: center;
}
</style>
