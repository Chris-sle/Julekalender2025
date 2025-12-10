<script setup>
import { ref, onMounted } from "vue"

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000"

const token = localStorage.getItem("authToken")
const entries = ref([])
const loading = ref(false)

const props = defineProps({
  onDelete: Function
})


async function loadAll() {
  loading.value = true

  const response = await fetch(`${API_BASE_URL}/calendar`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  loading.value = false

  if (!response.ok) {
    console.error("Feil ved henting av lister")
    return
  }

  entries.value = await response.json()
}


onMounted(() => {
  loadAll()
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Alle luker</h1>

    <button
        class="mb-4 px-4 py-2 bg-blue-600 text-white rounded"
        @click="loadAll"
    >
      Oppdater liste
    </button>

    <div v-if="loading">Laster...</div>

    <table v-else class="w-full border text-left">
      <thead class="bg-gray-200">
      <tr>
        <th class="p-2 border">Dato</th>
        <th class="p-2 border">Tekst</th>
        <th class="p-2 border">Video-type</th>
        <th class="p-2 border">Video-path</th>
        <th class="p-2 border w-40">Actions</th>
      </tr>
      </thead>

      <tbody>
      <tr v-for="entry in entries" :key="entry.id">
        <td class="p-2 border">{{ entry.date }}</td>
        <td class="p-2 border">{{ entry.task_text }}</td>
        <td class="p-2 border">{{ entry.video_type }}</td>
        <td class="p-2 border break-all">{{ entry.video_path }}</td>

        <td class="p-2 border">
          <button
              class="px-2 py-1 bg-green-600 text-white rounded mr-2"
              @click=""
          >
            Rediger
          </button>

          <button
              class="px-2 py-1 bg-red-600 text-white rounded"
              @click="props.onDelete(entry)"
          >
            Slett
          </button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>
