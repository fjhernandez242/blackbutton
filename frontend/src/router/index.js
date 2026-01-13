import { createRouter, createMemoryHistory } from 'vue-router'

const router = createRouter({
    history: createMemoryHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            component: () => import('../components/catalogo.vue')
        },
        {
            path: '/panel',
            component: () => import('../components/panel.vue')
        },
    ],
})

export default router
