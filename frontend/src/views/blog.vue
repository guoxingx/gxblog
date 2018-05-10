
<template>
  <div class="blog-main">
    <div v-html="html" class="html"></div>
    <div class="blog-main-footer">
      <el-tag class="tag" v-for="tag in tags" :key="tag" type="success">{{ tag }}</el-tag>
      <h4 class="date">{{ date }}</h4>
    </div>
    <div id="commentsContainer"></div>
  </div>
</template>

<script type="text/javascript">
import { getBlog, getHtml } from '@/js/requests'
import { gitmentConfig } from '@/js/gitmentConfig'
import Gitment from 'gitment'
import 'gitment/style/default.css'

export default {
  data () {
    return {
      blogId: null,
      title: '',
      date: '',
      html: '',
      tags: [],
      blogimg: ''
    }
  },

  created () {
    this.requestBlog()
  },

  methods: {
    requestBlog () {
      this.blogId = this.$route.params.id
      getBlog(this.blogId).then(res => {
        if (res.status === 200 && res.data.code === 0) {
          var data = res.data.data
          this.blogimg = data.image
          this.tags = data.tags
          this.title = data.title
          this.date = data.created_at

          getHtml(data.path).then(response => {
            this.html = response.data
            document.body.className = 'fixme'
          })
        }
      })
    },

    gitmentRender () {
      console.log(gitmentConfig)
      const gitment = new Gitment({
        id: this.$route.path,
        owner: gitmentConfig.owner,
        repo: gitmentConfig.repo,
        oauth: gitmentConfig.oauth
      })
      gitment.render('commentsContainer')
    }
  },

  watch: {
    '$route' (to, from) {
      this.html = ''
      this.blogimg = ''
      this.tags = []
      this.title = ''
      this.date = ''
      this.requestBlog()
      this.gitmentRender()
    }
  },
  beforeRouteEnter (to, from, next) {
    window.document.title = 'GXBlog'
    next(vm => { vm.gitmentRender() })
  },
  beforeRouteUpdate (to, from, next) {
    next()
  }
}

</script>

<style>
h1 {
  margin-top: 0px;
  padding-top: 20px;
}
.tag {
  margin-left: 10px;
}
.date {
  margin-left: 10px;
}
.fixme {
  max-width: 100%;
  margin: 0 auto;
  padding: 15px;
}
.blog-main {
  margin: 0 auto;
  max-width: 800px;
}
.blog-main-footer {
  margin-top: 10px;
  text-align: right;
}
.gitment-comment-main {
  background: white;
}
.gitment-editor-main {
  background: white;
}
</style>
