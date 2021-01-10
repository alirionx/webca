import Vue from 'vue'
import VueRouter from 'vue-router'
import Authorities from '../views/Authorities.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Authorities',
    component: Authorities
  },
  {
    path: '/logout',
    name: 'Logout',
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/Logout.vue')
    }
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})
/*
router.beforeEach((to, from, next) => {
  if (to.name !== 'Login' && !isAuthenticated) next({ name: 'Login' })
  else next()
})
*/

export default router
