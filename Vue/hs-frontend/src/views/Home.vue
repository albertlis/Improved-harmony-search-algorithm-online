<template>
    <v-container fill-height>
      <v-row justify="center">
        <v-col align="center">
          <v-img
          alt="Harmony search Logo"
          contain
          src="../assets/logoHS.png"
          transition="scale-transition"
          width="150"
          />
          <h1>Improved harmony search algorithm</h1>
          <p>
            is a metaheurestic alghoritm for solving problems. In this webpage it can solve linear and non linear equations.
          </p>
          <PopUp/>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-card flat>
          <v-card class="ma-1" >
              <div class="ma-1">
              <b>Known issues:</b>
              <ul>
                <!-- <li>Countour plot sometimes may be rotated</li> -->
                <!-- <li>Plot labels are not accurate</li> -->
                <li class="error--text">Backend service is temporarily turned off</li>
              </ul>
              </div>
          </v-card>
        </v-card>
      </v-row>
    </v-container> 
</template>

<script>
import PopUp from '@/components/PopUp'
export default {
  name: 'Home',
  components: {
    PopUp
  }
}
</script>
