<template>
  <div>
    <h1>{{ title }}</h1>
    <el-tag class="tag" v-for="tag in tags" type="success">{{ tag }}</el-tag>
    <div class="blog" v-html="html_content"></div>
    <h3 class="date">{{ date }}</h3>
  </div>
</template>

<script type="text/javascript">
import { getArticle } from '../requests'
import marked from 'marked'
import highlightjs from 'highlight.js'
import 'highlight.js/styles/googlecode.css'

marked.setOptions({
  renderer: new marked.Renderer(),
  gfm: true,
  tables: true,
  breaks: false,
  pedantic: false,
  sanitize: false,
  smartLists: true,
  smartypants: false,
  highlight: function (code) {
    return highlightjs.highlightAuto(code).value
  }
})

export default {
  components: {
    'wHeader': () => import('./components/header.vue'),
    marked,
    highlightjs
  },

  data () {
    return {
      html_content: 'sorry, nothing here.'
    }
  },

  created () {
    var aid = this.$route.params['id']
    axios.get(API_ROOT + 'api/articles/' + aid).then(res => {
      var content = marked(res.data.content, { sanitize: true })
      this.html_content = content
      this.blogimg = res.data.image
      this.tags = res.data.tags
      this.title = res.data.title
      this.date = res.data.date ? res.data.date : '2017.11.19'
    })
  }
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/blog.css';
</style>