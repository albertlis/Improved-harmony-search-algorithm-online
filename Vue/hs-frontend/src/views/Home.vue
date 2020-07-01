<template>
    <v-container fill-height>
      <v-row justify="center" align="center">
        <PopUp/>
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
