import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: () => import('../views/login.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/signup.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/user/dashboard.vue')
    },
    {
      path: '/dashboard/book',
      name: 'book',
      component: () => import('../views/user/book.vue')
    },
    {
      path: '/dashboard/profile',
      name: 'profile',
      component: () => import('../views/user/profile.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin/admin.vue')
    },
    {
      path: '/addLocation',
      name: 'addLocation',
      component: () => import('../views/admin/addLocation.vue')
    },
    {
      path: '/admin/users',
      name: 'users',
      component:() =>import('../views/admin/users.vue')
    },
    {
      path:'/admin/search',
      name:'search',
      component:()=>import('../views/admin/search.vue')

    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    },
  ]
})


router.beforeEach((to, from, next) => {
  const publicPages = ['login', 'signup']
  const authRequired = !publicPages.includes(to.name)
  const token = localStorage.getItem('token')

  if (authRequired && !token) {
    return next({ name: 'login' })
  }

  next()
})

export default router
