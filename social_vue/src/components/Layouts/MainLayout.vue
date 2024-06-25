<template>
  <div>
    <div class="layout">
      <NavBar />
      <div class="grow">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  components: {
    NavBar,
  },
};
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.border {
  width: 1px;
  background-color: #e9e9e5;
}

.grow {
  flex-grow: 1;
  overflow: scroll;
  padding: 0px;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
