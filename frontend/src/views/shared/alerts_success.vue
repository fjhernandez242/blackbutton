<template>
    <div class="notification-container">
        <TransitionGroup name="list" tag="div">
            <div
                v-for="notification in store.notifications"
                :key="notification.id"
                class="alert-item"
                >
                {{ notification.mensaje }}
                <button @click="store.eliminarAlerta(notification.id)">x</button>
            </div>
        </TransitionGroup>
    </div>
</template>

<script setup>
    import { useNotificationStore } from '@/store/notificationStore';
    const store = useNotificationStore();
</script>

<style scoped>
    .notification-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        z-index: 9999;
    }

    .alert-item {
        background-color: rgb(238, 247, 255);
        color: black;
        padding: 1rem;
        margin-top: 5px;
        border-radius: 8px;
        min-width: 200px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
    }

    /* Animaciones de Vue */
    .list-enter-active, .list-leave-active {
        transition: all 0.5s ease;
    }
    .list-enter-from {
        opacity: 0;
        transform: translateX(30px);
    }
    .list-leave-to {
        opacity: 0;
        transform: scale(0.9);
    }

    button {
        border: none;
        border-radius: 8px;
        background: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>