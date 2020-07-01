<template>
  <v-app>
    <NavBar/>
    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
// import HelloWorld from './components/HelloWorld';
import NavBar from './components/NavBar';

export default {
  name: 'App',

  components: {
    // HelloWorld,
    NavBar
  },

  data: () => ({
    //
  }),
};
</script>
