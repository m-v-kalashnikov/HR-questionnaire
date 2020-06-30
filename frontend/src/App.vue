<template>
  <div id="app">
    <navbar></navbar>
    <router-view></router-view>
  </div>
</template>

<script>

import Navbar from './components/Navbar';

export default {
  name: 'app',
  components: {
    Navbar,
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.btn-vue {
  color: #2c3e50 !important;
  background-color: #42b983 !important;
  border-color: #3ba775 !important;
}
.btn-vue:hover {
  color: #2c3e50 !important;
  background-color: #35976b !important;
  border-color: #318b61 !important;
}

.btn-vue:focus, .btn-vue.focus {
  color: #2c3e50 !important;
  background-color: #35976b;
  border-color: #318b61 !important;
  box-shadow: 0 0 0 0.2rem rgba(72, 180, 97, 0.5) !important;
}

.btn-vue.disabled, .btn-vue:disabled {
  color: #2c3e50 !important;
  background-color: #267451 !important;
  border-color: #256f4c !important;
}

.btn-vue:not(:disabled):not(.disabled):active, .btn-vue:not(:disabled):not(.disabled).active,
.show > .btn-vue.dropdown-toggle {
  color: #2c3e50 !important;
  background-color: #267451 !important;
  border-color: #256f4c !important;
}

.btn-vue:not(:disabled):not(.disabled):active:focus, .btn-vue:not(:disabled):not(.disabled).active:focus,
.show > .btn-vue.dropdown-toggle:focus {
  box-shadow: 0 0 0 0.2rem rgba(72, 180, 97, 0.5) !important;
}
.bg-vue-dark {
  background: #2c3e50 !important;
}
</style>
