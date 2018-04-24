
<template>
  <div class="main">
    <h1>{{ title }}</h1>
    <el-tag class="tag" v-for="tag in tags" :key="tag" type="success">{{ tag }}</el-tag>
    <h4 class="date">{{ date }}</h4>
    <div v-html="html" class="html" id="html"></div>
  </div>
</template>

<script type="text/javascript">
import { getArticle, getHtml } from '../requests'

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
    var aid = this.$route.params.id
    getArticle(aid).then(res => {
      this.blogimg = res.data.image
      this.tags = res.data.tags
      this.title = res.data.title
      this.date = res.data.date ? res.data.date : '2017.11.19'

      getHtml(res.data.html).then(response => {
        console.log(response.data)
        this.html = response.data
      })
    })
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
</style>
