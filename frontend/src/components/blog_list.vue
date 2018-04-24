<template>

  <div>
    <div class="articles">
      <blog-cell v-for="article in articles" :key="article" :unit="article"></blog-cell>
    </div>
  </div>

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
      articles: null
    }
  },
  created () {
    getArticleList().then(res => {
      this.articles = res.data
    })
  },

  methods: {
    scrollEvent () {
      var h2top = document.body.scrollTop === 0 ? document.documentElement.scrollTop : document.body.scrollTop

      console.log(window.innerHeight + h2top, document.body.clientHeight)

      if (window.innerHeight + h2top >= document.body.clientHeight) {
        this.loadmore()
      }
    },

    loadmore () {
      console.log('loadmore')
    }
  },

  mounted () {
    window.addEventListener('scroll', this.scrollEvent)
  },

  destroyed () {
    window.removeEventListener('scroll', this.scrollEvent)
  }

}
</script>
