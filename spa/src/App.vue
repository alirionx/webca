<template>
  <div id="app">
    <HeadBlock />
    <router-view/>
  </div>
</template>

<script>
import HeadBlock from './components/HeadBlock.vue'
export default {
  name: 'Main',
  components: {
    HeadBlock
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-top:120px;

}

</style>
