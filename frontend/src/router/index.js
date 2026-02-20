import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'catalogo',
            component: () => import('../views/catalogo.vue'),
            meta: { hideHeader: false }
        },
        {
            path: '/panel',
            name: 'panel',
            component: () => import('../views/panel.vue'),
            meta: { hideHeader: true }
        },
    ],
})

export default router
