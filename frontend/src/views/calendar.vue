<template>
  <div class="calendar-view relative min-h-screen flex flex-col">
    <!-- Snow stuff -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden z-0">
      <div
        v-for="flake in snowflakes"
        :key="flake.id"
        class="snowflake"
        :style="{
          left: flake.left + '%',
          animationDuration: flake.duration + 's',
          width: flake.size + 'px',
          height: flake.size + 'px',
          opacity: flake.opacity
        }"
      ></div>
    </div>

    <!-- Calendar grid -->
    <div class="flex-1 grid grid-cols-4 gap-4 p-6"
         :style="{ backgroundImage: `url(${bg})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
      <Card
        v-for="day in days"
        :key="day.number"
        :day="day.number"
        :opened="openedDays.includes(day.number)"
        @open="openCard"
      />
    </div>

    <!-- Modal -->
    <CardModal
      :show="selectedDay !== null"
      @opened="modalOpened"
      @close="closeCard"
    >
        <h2 class="day-label">{{ selectedDay }}. Desember</h2>
        <div v-if="currentEntry" class="modal-content">
        <p v-if="currentEntry.task_text" class="task-content">{{ currentEntry.task_text }}</p>
        
        <!-- YouTube video -->
        <div v-if="currentEntry.video_type === 'youtube' && currentEntry.video_path" class="w-full">
          <iframe
            :src="`https://www.youtube.com/embed/${extractYoutubeId(currentEntry.video_path)}`"
            width="100%"
            height="315"
            frameborder="0"
            allowfullscreen
          ></iframe>
        </div>
        
      <!-- Uploaded video/content -->
      <div v-if="currentEntry.video_type === 'upload' && currentEntry.video_path" class="w-full">
        <template v-if="isVideo(currentEntry.video_path)">
          <video width="100%" controls>
            <source :src="getUploadUrl(currentEntry.video_path)" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </template>
        <template v-else>
          <img
            :src="getUploadUrl(currentEntry.video_path)"
            alt="Uploaded content"
            class="w-full object-contain"
          />
        </template>
      </div>
      </div>
      <p v-else class="text-center text-gray-500">Innholdet kommer snart...</p>
    </CardModal>

    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Card from '../components/Cards.vue'
import CardModal from '../components/CardModal.vue'
import Footer from '../components/Footer.vue'
import bg from '../img/background2.jpg'

 const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// Opened cards
const openedDays = ref([])
const selectedDay = ref(null)
const currentEntry = ref(null)

// Snowflake data
const snowflakes = Array.from({ length: 50 }, (_, i) => ({
  id: i,
  left: Math.random() * 100,
  duration: 5 + Math.random() * 5,
  size: 4 + Math.random() * 4,
  opacity: 0.4 + Math.random() * 0.6
}))

function extractYoutubeId(url) {
  const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/
  const match = url.match(regex)
  return match ? match[1] : ''
}

async function fetchEntryForDay(day) {
  try {
    const year = new Date().getFullYear()
    const month = 12 // December
    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    
    const visitorToken = localStorage.getItem('visitorToken')
    const headers = {}
    if (visitorToken) headers['X-Visitor-Token'] = visitorToken

    const url = `${API_BASE_URL}/calendar/${dateStr}`
    console.log('[Calendar] Fetching entry for', dateStr, url)
    const response = await fetch(url, { method: 'GET', headers })
    console.log('[Calendar] Fetch response', response.status, response.statusText)
    if (response.ok) {
      const data = await response.json()
      currentEntry.value = data
      if (data && data.video_type === 'upload' && data.video_path) {
        console.log('[Calendar] Raw video_path from backend:', data.video_path)
        const filename = data.video_path.split(/[/\\]/).pop()
        const videoUrl = `${API_BASE_URL}/uploads/${encodeURIComponent(filename)}`
        console.log('[Calendar] Uploaded video URL:', videoUrl)
      }
    } else {
      currentEntry.value = null
    }
  } catch (error) {
    console.error('Failed to fetch calendar entry:', error)
    currentEntry.value = null
  }
}

function openCard(day) {
  const today = new Date()
  const currentDay = today.getDate()

  // Lock future days
  if (day > currentDay) return

  // Open the modal
  selectedDay.value = day
  fetchEntryForDay(day)

  // Save in localStorage if not already opened
  if (!openedDays.value.includes(day)) {
    openedDays.value.push(day)
    localStorage.setItem('openedDays', JSON.stringify(openedDays.value))
  }
}


function closeCard() {
  selectedDay.value = null
  currentEntry.value = null
}

// Shuffle function
function shuffle(array){
  const arr = [...array];
  for(let i = arr.length - 1; i > 0; i--){
    const j = Math.floor(Math.random() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  return arr
}

let storedDays = localStorage.getItem('calendarDays')
const orderedDays = Array.from({ length: 24 }, (_, i) => ({ number: i + 1 }))
const days = ref(storedDays ? JSON.parse(storedDays) : shuffle(orderedDays))
if (!storedDays) localStorage.setItem('calendarDays', JSON.stringify(days.value))

let storedOpened = localStorage.getItem('openedDays')
if (storedOpened) openedDays.value = JSON.parse(storedOpened)

function isVideo(path) {
  const ext = path.split('.').pop().toLowerCase()
  return ['mp4', 'webm', 'ogg'].includes(ext)
}

function getUploadUrl(path) {
  const filename = path.split(/[/\\]/).pop()
  return `${API_BASE_URL}/uploads/${encodeURIComponent(filename)}`
}

function modalOpened() {
  // Placeholder for any action when modal is opened
}
</script>


<style scoped>
.snowflake {
  position: absolute;
  top: -10px;
  background: white;
  border-radius: 50%;
  animation-name: fall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

@keyframes fall {
  0% { transform: translateY(0) translateX(0); }
  50% { transform: translateY(50vh) translateX(10px); }
  100% { transform: translateY(100vh) translateX(-10px); }
}

.modal-content {
  flex: 1;
  overflow-y: auto;
  padding: clamp(0.5rem, 2vw, 1rem);
  border-radius: clamp(0.4rem, 1.5vw, 0.6rem);
  display: flex;
  flex-direction: column;
  max-width: 100%;
  overflow-x: hidden;
}

.modal-card .day-label {
  background: #fdf8e7;
  padding: clamp(0.75rem, 5vw, 1.25rem) clamp(1rem, 6vw, 1.5rem);
  border-radius: clamp(0.5rem, 2vw, 0.75rem);
  display: inline-block;
  color: #3b2f1e;
  font-weight: 600;
  font-size: clamp(1.1rem, 4vw, 1.4rem);
  font-family: 'Georgia', serif;
  position: relative;
  box-shadow: 0 clamp(2px, 1vw, 8px) clamp(4px, 2vw, 12px) rgba(0,0,0,0.25);
  background-image: radial-gradient(rgba(0, 0, 0, 0.04) 1px, transparent 1px);
  background-size: 6px 6px;
  margin-bottom: clamp(1rem, 4vw, 2rem);
}

.modal-card .day-label::before {
  content: "";
  position: absolute;
  top: 0;
  left: clamp(-8px, -1.5vw, -12px);
  width: 0;
  height: 0;
  border-top: clamp(8px, 1.5vw, 12px) solid transparent;
  border-bottom: clamp(8px, 1.5vw, 12px) solid transparent;
  border-right: clamp(8px, 1.5vw, 12px) solid #fdf8e7;
}

.modal-card .task-content {
  background: #fdf8e7;
  padding: clamp(0.65rem, 4vw, 1.15rem) clamp(0.9rem, 5vw, 1.4rem);
  border-radius: clamp(0.5rem, 2vw, 0.75rem);
  display: block;
  max-width: 100%;
  color: #3b2f1e;
  font-weight: 500;
  font-size: clamp(0.95rem, 3.5vw, 1.15rem);
  font-family: 'Georgia', serif;
  position: relative;
  box-shadow: 0 clamp(2px, 1vw, 8px) clamp(4px, 2vw, 12px) rgba(0,0,0,0.25);
  background-image: radial-gradient(rgba(0, 0, 0, 0.04) 1px, transparent 1px);
  background-size: 6px 6px;
  margin-bottom: clamp(0.75rem, 3vw, 1.5rem);
  line-height: clamp(1.4, 2vw, 1.8);
  white-space: normal;
  overflow-wrap: break-word;
  word-break: break-word;
}

.modal-card .task-content::before {
  content: "";
  position: absolute;
  top: 0;
  left: clamp(-8px, -1.5vw, -12px);
  width: 0;
  height: 0;
  border-top: clamp(8px, 1.5vw, 12px) solid transparent;
  border-bottom: clamp(8px, 1.5vw, 12px) solid transparent;
  border-right: clamp(8px, 1.5vw, 12px) solid #fdf8e7;
}


</style>
