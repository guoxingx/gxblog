<template>
  <div>
    <vue-headful title="GXBlog"/>
    <el-row>
      <el-col :xs="2" :sm="2" :md="2" :lg="3" :xl="4">
        <div class="space left"></div>
      </el-col>
      <el-col :xs="20" :sm="19" :md="17" :lg="14" :xl="12">
        <div class="blogs">
          <blog-cell v-for="blog in blogs" :key="blog" :blog="blog"></blog-cell>
        </div>
      </el-col>
      <el-col :xs="2" :sm="3" :md="5" :lg="7" :xl="8">
        <div class="space right"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getBlogList } from '@/js/requests'

export default {
  name: 'blog_list',
  components: {
    'blog-cell': () => import('../components/blog_cell.vue')
  },
  data () {
    return {
      blogs: []
    }
  },
  created () {
    getBlogList().then(res => {
      if (res.data.code === 0) {
        this.blogs = res.data.data
      }
    })
  }
}
</script>

<style>
.blogs {
  text-align: center;
}
.space {
  min-height: 100px;
}
</style>
