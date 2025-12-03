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
      <h2 class="text-xl font-bold mb-4 text-center">
        Dag {{ selectedDay }}
      </h2>
      <p>Her kommer det masse greier etterhvert!</p>
    </CardModal>

    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Card from '../components/Cards.vue'
import CardModal from '../components/CardModal.vue'
import Footer from '../components/Footer.vue'
import bg from '../img/background.jpg'

// opened cards
const openedDays = ref([])
const selectedDay = ref(null)

// snowflake data
const snowflakes = Array.from({ length: 50 }, (_, i) => ({
  id: i,
  left: Math.random() * 100,
  duration: 5 + Math.random() * 5,
  size: 4 + Math.random() * 4,
  opacity: 0.4 + Math.random() * 0.6
}))

function openCard(day) {
  selectedDay.value = day
}

function closeCard() {
  if (selectedDay.value && !openedDays.value.includes(selectedDay.value)) {
    openedDays.value.push(selectedDay.value)
    // save openedDays in localStorage so it persists
    localStorage.setItem('openedDays', JSON.stringify(openedDays.value))
  }
  selectedDay.value = null
}

function modalOpened() {
  // placeholder for modal actions
}

// shuffle helper
function shuffle(array){
  const arr = [...array];
  for(let i = arr.length - 1; i > 0; i--){
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// days array (shuffled, persisted)
let storedDays = localStorage.getItem('calendarDays')
const orderedDays = Array.from({ length: 24 }, (_, i) => ({ number: i + 1 }))

const days = ref(storedDays ? JSON.parse(storedDays) : shuffle(orderedDays))

// save days in localStorage if first load
if (!storedDays) localStorage.setItem('calendarDays', JSON.stringify(days.value))

// restore openedDays from localStorage
let storedOpened = localStorage.getItem('openedDays')
if (storedOpened) openedDays.value = JSON.parse(storedOpened)
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
</style>
