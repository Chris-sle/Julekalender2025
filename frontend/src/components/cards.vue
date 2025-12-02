<template>
  <div
    class="card"
    :class="{ opened }"
    @click="open"
  >
    <span class="number">{{ day }}</span>
  </div>
</template>

<script>
export default {
  name: "Cards",
  props: {
    day: Number,
    opened: Boolean
  },
  emits: ["open"],
  methods: {
    open() {
      if (!this.opened) this.$emit("open", this.day)
    }
  }
}
</script>

<style scoped>
.card {
  width: 90px;
  height: 90px;
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-right: 2px dashed rgba(255,255,255,0.8);
  background-color: transparent;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform .2s, box-shadow .2s;
  clip-path: polygon(
    0 0, 100% 0, 100% 10%, 95% 15%, 100% 20%, 95% 25%, 100% 30%, 95% 35%, 100% 40%, 100% 100%, 0 100%
  );
}



/* Hover effect */
.card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}

/* Opened card style */
.opened {
  opacity: 0.6;
}

/* Card number */
.number {
  font-size: 2rem;
  font-weight: bold;
  color: white;
  text-shadow: 0 0 6px black;
}
</style>
