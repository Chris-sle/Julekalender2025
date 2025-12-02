<template>
  <transition name="modal">
    <div v-if="show" class="modal-bg" @click="$emit('close')">
      <div class="modal-card" @click.stop>
        <slot />
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    show: Boolean
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity .3s, transform .3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.7);
}

.modal-bg {
  position: fixed;
  inset: 0;
  background: transparent; 
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-card {
  background: rgb(82, 81, 81);
  width: 300px;
  padding: 20px;
  border-radius: 12px;
}
</style>
