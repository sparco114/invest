import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import AssetsView from '../views/AssetsView.vue'
import OperationsView from '../views/OperationsView.vue'
import ProfileEditView from '../views/ProfileEditView.vue'


import ProfileDetailView from '../views/ProfileDetailView.vue'
import UserRegistrationView from '../views/UserRegistrationView.vue'
import UserLogInView from '../views/UserLogInView.vue'
import NotFound from '../views/NotFound.vue'
import AboutProject from '../views/AboutProject.vue'
import Agreement from '../views/Agreement.vue'
import ConfidentialPolicy from '../views/ConfidentialPolicy.vue'
import Support from '../views/Support.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },    
    {
      path: '/statistics',
      name: 'statistics-list',
      component: StatisticsView
    },
    {
      path: '/assets',
      name: 'assets-list',
      component: AssetsView
    },
    {
      path: '/operations',
      name: 'operations-list',
      component: OperationsView
    },
    {
      path: '/profiles/:id',
      name: 'profile-detail',
      component: ProfileDetailView
    },
    {
      path: '/registration',
      name: 'user-registration',
      component: UserRegistrationView
    },
    {
      path: '/login',
      name: 'user-login',
      component: UserLogInView
    },
    {
      path: '/profiles/my/edit',
      name: 'profile-edit',
      component: ProfileEditView
    },
    {
      path: '/404',
      name: 'not-found-page',
      component: NotFound
    },
    { path: '/:pathMatch(.*)*',
      name: 'not-found-path', 
      component: NotFound 
    },
    {
      path: '/about-project',
      name: 'about-project',
      component: AboutProject
    },
    {
      path: '/agreement',
      name: 'agreement',
      component: Agreement
    },
    {
      path: '/confidential-policy',
      name: 'confidential-policy',
      component: ConfidentialPolicy
    },
    {
      path: '/support',
      name: 'support',
      component: Support
    },
    

    
    // Динамический импорт
    // {
    //   path: '/example',
    //   name: 'example',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/ExampleView.vue')
    // }
  ],

// TODO: страницы не всегда открываются с начала(сверху). Попробовать решить это другим способом.
  scrollBehavior() {
    return { top: 0 }; // Прокрутка страницы в начало при каждом переходе
  },
})

export default router
