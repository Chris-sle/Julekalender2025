<script setup>
import { ref, onMounted } from "vue"

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000"
const token = localStorage.getItem("authToken")
const entries = ref([])
const loading = ref(false)

const props = defineProps({
  onDelete: Function
})

const emit = defineEmits(['edit'])

async function loadAll() {
  loading.value = true
  try {
      const response = await fetch(`${API_BASE_URL}/calendar`, {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (!response.ok) throw new Error("Feil ved henting");
      entries.value = await response.json()
  } catch (e) {
      console.error(e);
  } finally {
      loading.value = false
  }
}

function getYoutubeEmbed(url) {
    if (!url) return "";
    const match = url.match(/(?:v=|\/embed\/|\/shorts\/|youtu\.be\/|\/v\/)([^?&\/\s]{11})/i);
    return match && match[1] ? `https://www.youtube.com/embed/${match[1]}` : url;
}

// Vi må vite hele URL-en til backend for å vise bilder/video hvis de er relative stier
function getFullMediaUrl(url) {
    if (!url) return "";
    if (url.startsWith("http")) return url; // Allerede full URL (f.eks youtube)
    return `${API_BASE_URL}${url}`; // Legg til http://localhost:5000 foran /uploads/...
}

function isImage(path) {
    const ext = path?.split('.').pop().toLowerCase();
    return ['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext);
}

// Eksponer loadAll så forelder kan kalle den etter lagring
defineExpose({ loadAll })

onMounted(loadAll)
</script>

<template>
  <div class="bg-white rounded-lg shadow-lg p-6 h-full">
    <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Alle luker ({{ entries.length }})</h2>
        <button class="px-3 py-1 bg-blue-100 text-blue-800 rounded hover:bg-blue-200 text-sm" @click="loadAll">
            🔄 Oppdater
        </button>
    </div>

    <div v-if="loading" class="text-gray-500 text-center py-10">Laster kalender...</div>

    <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
          <tr>
            <th class="p-3 border-b">Dato</th>
            <th class="p-3 border-b">Innhold</th>
            <th class="p-3 border-b">Media</th>
            <th class="p-3 border-b text-right">Handling</th>
          </tr>
          </thead>
          <tbody class="text-sm">
          <tr v-for="entry in entries" :key="entry.id" class="hover:bg-gray-50 border-b last:border-0">
            
            <!-- Dato -->
            <td class="p-3 font-medium whitespace-nowrap align-top">
                {{ entry.date }}
                <span v-if="!entry.is_published" class="block text-xs text-red-500 mt-1">Upublisert</span>
            </td>

            <!-- Tekst -->
            <td class="p-3 align-top max-w-xs">
                <div class="truncate max-h-20 whitespace-pre-wrap">{{ entry.task_text }}</div>
            </td>

            <!-- Media (Video/Bilde) -->
            <td class="p-3 align-top w-48">
                <div v-if="entry.video_type === 'youtube'" class="aspect-video bg-black rounded overflow-hidden">
                    <iframe :src="getYoutubeEmbed(entry.video_url)" class="w-full h-full" frameborder="0"></iframe>
                </div>
                <div v-else-if="entry.video_type === 'upload' && entry.video_url" class="aspect-video bg-gray-200 rounded overflow-hidden flex items-center justify-center">
                    <video v-if="!isImage(entry.video_url)" controls class="w-full h-full object-cover">
                        <source :src="getFullMediaUrl(entry.video_url)" />
                    </video>
                    <img v-else :src="getFullMediaUrl(entry.video_url)" class="w-full h-full object-cover" />
                </div>
                <span v-else class="text-gray-400 italic">Ingen media</span>
            </td>

            <!-- Knapper -->
            <td class="p-3 align-top text-right whitespace-nowrap">
              <button @click="$emit('edit', entry)" class="text-blue-600 hover:text-blue-800 mr-3 font-medium">
                Rediger
              </button>
              <button @click="props.onDelete(entry)" class="text-red-600 hover:text-red-800 font-medium">
                Slett
              </button>
            </td>

          </tr>
          <tr v-if="entries.length === 0">
              <td colspan="4" class="p-6 text-center text-gray-500">Ingen luker opprettet ennå.</td>
          </tr>
          </tbody>
        </table>
    </div>
  </div>
</template>