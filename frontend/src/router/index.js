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
            path: '/login_panel',
            name: 'login_panel',
            component: () => import('../views/login_panel.vue'),
            meta: { hideHeader: true }
        },
        {
            path: '/panel',
            name: 'panel',
            component: () => import('../views/panel.vue'),
            meta: { hideHeader: true, requiresAuth: true }
        },
    ],
})

router.beforeEach((to, from, next) => {
    // Busca el token del administrador
    const tokenAdmin = localStorage.getItem('admin_token');
    const tiempoExpiracion = localStorage.getItem('admin_token_expires');
    const tiempoActual = Date.now();

    // Verificamos si el token ya expiró
    const sesionExpirada = tiempoExpiracion && tiempoActual > parseInt(tiempoExpiracion);
    if (sesionExpirada) {
        // Si ya expiro, borramos los residuos del localStore
        localStorage.removeItem('admin_token');
        localStorage.removeItem('admin_token_expires');

        // Si ya va hacia el login, déja pasar para que no cicle
        if (to.name === 'login_panel') return next();
        // Lo mandamos al login avisando
        return next({ name: 'login_panel', query: { mensaje: 'sesion_expirada' } });
    }
    // Si la ruta requiere autenticación y NO hay token
    if (to.matched.some(record => record.meta.requiresAuth) && !tokenAdmin) {
        // Se rebota de inmediato al formulario de login
        next({ name: 'login_panel' });
    }
    // Si el usuario ya está logueado e intenta entrar al login de nuevo
    else if (to.name === 'login_panel' && tokenAdmin) {
        // Se manda directo al panel de administrador
        next({ name: 'panel' });
    }
    // Libre acceso
    return next();
});

export default router
