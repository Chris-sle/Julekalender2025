<template>
  <footer class="bg-gray-800 text-white p-2 flex items-center justify-between text-sm">
    <div>
      &copy; 2025 Julekalender — <i>Christopher S, Christopher K og Rune S</i>
    </div>

    <div class="flex gap-2">
      <!-- Vis "Til Kalender" hvis vi er på admin-siden -->
      <button
        v-if="isOnAdminPage"
        class="px-3 py-1 bg-blue-600 rounded hover:bg-blue-500 text-sm"
        @click="goToCalendar"
      >
        Til Kalender
      </button>

      <!-- Vis "Admin" hvis man er på kalender-siden (eller login) -->
      <button
        v-else
        class="px-3 py-1 bg-gray-600 rounded hover:bg-gray-500 text-sm"
        @click="goToAdmin"
      >
        Admin
      </button>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// Sjekker om nåværende sti starter med '/admin'
const isOnAdminPage = computed(() => {
  return route.path.startsWith('/admin');
});

function goToAdmin() {
  router.push('/admin');
}

function goToCalendar() {
  router.push('/');
}
</script>