<template>
  <v-app-bar
      app
      color="primary"
      dark
      dense
    >
      <v-spacer></v-spacer>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="30"
        />
        <v-toolbar-title>Harmony search alghoritm</v-toolbar-title>
      </div>
      <v-spacer></v-spacer>
    </v-app-bar>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>