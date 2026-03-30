import { createRouter, createWebHistory } from 'vue-router'
import StrategiesPage from '../pages/StrategiesPage.vue'
import StrategyEditorPage from '../pages/StrategyEditorPage.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/strategies',
    },
    {
      path: '/strategies',
      name: 'Strategies',
      component: StrategiesPage,
    },
    {
      path: '/strategies/new',
      name: 'StrategyNew',
      component: StrategyEditorPage,
    },
    {
      path: '/strategies/:strategyid',
      name: 'StrategyEdit',
      component: StrategyEditorPage,
    },
  ],
})

