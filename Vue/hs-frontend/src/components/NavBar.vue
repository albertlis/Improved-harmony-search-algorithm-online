<template>
  <v-app-bar
      app
      color="primary"
      dark
      dense
    >
      <v-spacer></v-spacer>
      <div class="d-flex align-center">
        <v-btn text href="/">
          <v-img
            alt="HS Logo"
            class="shrink mr-1"
            contain
            src="../assets/logoHS.png"
            transition="scale-transition"
            width="50" 
          />
          <v-toolbar-title>IHS algorithm</v-toolbar-title>
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