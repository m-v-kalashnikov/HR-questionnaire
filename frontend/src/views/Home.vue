<template>
  <div class="home mt-3">
    <img alt="Question logo" src="../assets/logo.png">
    <HelloWorld msg="Добро пожаловать к нам на огонёк!"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'Home',
  components: {
    HelloWorld,
  },
};
</script>

<style>
.home {
  text-align: center;
}
</style>
