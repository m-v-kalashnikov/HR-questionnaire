<template>
  <div id="lost-view">
    <h1>Page Not Found</h1>
    <h4>One of us is lost.</h4>
    <router-link to="/">Take me home.</router-link>
  </div>
</template>

<script>
export default {
  name: 'lost',
};
</script>

<style>
#lost-view {
  min-height: calc(100vh - 66px);
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
</style>
