<template>
  <footer class="bg-gray-800 text-white p-2 flex items-center justify-between text-sm">
    <div>
      &copy; 2025 Julekalender — <i>Christopher S, Christopher K og Rune S</i>
    </div>

    <div class="flex gap-2">
      <!-- Vis "Til Kalender" hvis vi er på admin-siden -->
      <template v-if="isOnAdminPage">
        <button class="px-3 py-1 bg-blue-600 rounded hover:bg-blue-500 text-sm" @click="goToCalendar">
          Til Kalender
        </button>

        <button class="px-3 py-1 bg-red-600 rounded hover:bg-red-500 text-sm" @click="logout">
          Logg ut
        </button>
      </template>

      <!-- Vis "Admin" hvis man er på kalender-siden (eller login) -->
      <button v-else class="px-3 py-1 bg-gray-600 rounded hover:bg-gray-500 text-sm" @click="goToAdmin">
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

const isOnLoginPage = computed(() => route.path === '/login'); // Skjul "Admin"-knapp på login-siden

function goToAdmin() {
  router.push('/admin');
}

function goToCalendar() {
  router.push('/');
}

function logout() {
  if (confirm("Er du sikker på at du vil logge ut?")) {
    localStorage.removeItem('authToken');
    router.push('/');
  }
}
</script>