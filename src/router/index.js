import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/experiment/:exp_id/:id',
    name: 'Experiment',
    props: true,
    component: () => import( '@/views/Experiment.vue')
  }, 
  {
    path: '/experiment/:exp_id',
    name: 'Settings',
    props: true,
    component: () => import('@/views/Experiment_Settings.vue')
  },
  {
    path: '/',
    name: '',
    // redirect: '/experiment',
    component: () => import('@/views/Home.vue')
  }, 
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
