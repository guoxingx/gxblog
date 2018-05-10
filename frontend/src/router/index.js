import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      redirect: '/blogs'
    },
    {
      path: '/blogs',
      name: 'blogs',
      component: function (resolve) {
        require(['@/views/blog_list'], resolve)
      },
      meta: { title: 'gxblog' }
    },
    {
      path: '/blogs/:id',
      name: 'blog',
      component: function (resolve) {
        require(['@/views/blog'], resolve)
      },
      meta: { title: 'gxblog' }
    },
    {
      path: '/betonether/:id',
      name: 'betonether',
      component: function (resolve) {
        require(['@/views/betonether'], resolve)
      },
      meta: { title: 'gxblog-betonether' }
    }
  ]
})
