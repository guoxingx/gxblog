
<template>
  <div class="blog-main">
    <vue-headful title="GXBlog"/>
    <div v-html="html" class="html" id="html"></div>
    <div class="blog-main-footer">
      <el-tag class="tag" v-for="tag in tags" :key="tag" type="success">{{ tag }}</el-tag>
      <h4 class="date">{{ date }}</h4>
    </div>
  </div>
</template>

<script type="text/javascript">
import { getBlog, getHtml } from '@/js/requests'

export default {
  template: '#tpl',
  data () {
    return {
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
      var aid = this.$route.params.id
      getBlog(aid).then(res => {
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
        } else {
          alert('fuck')
        }
      })
    }
  },

  watch: {
    '$route' (to, from) {
      this.requestBlog()
    }
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
  /*background: green;*/
  /*width: 100%;*/
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
</style>
