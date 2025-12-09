<template>
  <transition name="modal">
    <div v-if="show" class="modal-bg" @click="$emit('close')">
      <div
        class="modal-card festive-border"
        @click.stop
        :style="{
          backgroundImage: `url(${modalBg})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }"
      >
        <slot />
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    show: Boolean
  },
  data() {
    return {
      modalBg: new URL('../img/modalbackground.jpg', import.meta.url).href
    };
  }
};
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.7);
}

.modal-bg {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  background: rgba(82, 81, 81, 1);
  width: 90vw;
  max-width: 800px;
  max-height: 90vh;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.4);
  overflow-y: auto;
  z-index: 1001;
  position: relative;
}

.festive-border {
  border: 6px solid rgb(255, 0, 255);
  animation: christmas-border 10s infinite alternate;
  border-radius: 12px;
}

@keyframes christmas-border {
  0% { border-color: rgb(255, 255, 255); }
  25% { border-color: green; }
  50% { border-color: gold; }
  75% { border-color: rgb(44, 1, 94); }
  100% { border-color: rgb(31, 70, 248); }
}
</style>
