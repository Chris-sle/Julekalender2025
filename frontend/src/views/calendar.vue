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
        v-for="day in 24"
        :key="day"
        :day="day"
        :opened="openedDays.includes(day)"
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
  left: Math.random() * 100,           // random horizontal position
  duration: 5 + Math.random() * 5,     // 5-10s animation
  size: 4 + Math.random() * 4,         // 4-8px
  opacity: 0.4 + Math.random() * 0.6   // 0.4-1
}))

function openCard(day) {
  selectedDay.value = day
}

function closeCard() {
  if (selectedDay.value && !openedDays.value.includes(selectedDay.value)) {
    openedDays.value.push(selectedDay.value)
  }
  selectedDay.value = null
}

function modalOpened() {
  // kommer greier her etterhvert
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

/* Fall animation */
@keyframes fall {
  0% { transform: translateY(0) translateX(0); }
  50% { transform: translateY(50vh) translateX(10px); }
  100% { transform: translateY(100vh) translateX(-10px); }
}

</style>
