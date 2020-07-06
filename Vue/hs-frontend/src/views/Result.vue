<template>
    <v-container fill-height>
      <v-row align="center">
        <v-col align="center">
          <Plotly :data="data" :layout="layout" :display-mode-bar="false"></Plotly>
        </v-col>
      </v-row>
    </v-container> 
</template>

<script>
import { Plotly } from 'vue-plotly'
export default {
  name: 'Result',
  components: {
    Plotly
  },
  data:() => ({
    data:[{
      x: [1,2,3,4],
      y: [10,15,13,17],
      type:"scatter"
    }],
    layout:{
      title: "My graph"
    }
  })
}
</script>
