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
      }
    },
    {
      path: '/blogs/:id',
      name: 'blog',
      component: function (resolve) {
        require(['@/views/blog'], resolve)
      }
    },
    {
      path: '/betonether/:page',
      name: 'betonether',
      component: function (resolve) {
        require(['@/views/betonether'], resolve)
      }
    }
  ]
})
