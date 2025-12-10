<template>
  <footer class="bg-gray-800 text-white p-2 flex items-center justify-between text-sm">
    <div>
      &copy; 2025 Julekalender — <i>Christopher S, Christopher K og Rune S</i>
    </div>

    <div class="flex gap-2">
      <button
        class="px-3 py-1 bg-gray-600 rounded hover:bg-gray-500 text-sm"
        @click="$router.push('/admin')"
      >
        Admin
      </button>
    </div>
  </footer>
</template>

<script setup>
function resetCalendar() {
  localStorage.removeItem('openedDays')
  localStorage.removeItem('calendarDays')
  alert('Calendar reset! Refresh the page.')
}
</script>
