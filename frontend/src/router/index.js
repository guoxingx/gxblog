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
        require(['@/components/blog_list'], resolve)
      }
    },
    {
      path: '/hello',
      name: 'HelloWorld',
      component: function (resolve) {
        require(['@/components/HelloWorld'], resolve)
      }
    },
    {
      path: '/blogs/:id',
      name: 'blog',
      component: function (resolve) {
        require(['@/components/blog'], resolve)
      }
    },
    {
      path: '/betonether/:id',
      name: 'betonether',
      component: function (resolve) {
        require(['@/components/betonether'], resolve)
      }
    }
  ]
})
