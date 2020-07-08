<template>
  <v-app-bar
      app
      color="primary"
      dark
      dense
    >
      <v-spacer></v-spacer>
      <div class="d-flex align-center">
        <v-btn text to="/">
          <v-img to="/"
            alt="HS Logo"
            class="shrink mr-2"
            contain
            src="../assets/logoHS.png"
            transition="scale-transition"
            width="50"
            
          />
          <v-toolbar-title>Harmony search alghoritm</v-toolbar-title>
        </v-btn>
      </div>
      <v-spacer></v-spacer>
    </v-app-bar>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>