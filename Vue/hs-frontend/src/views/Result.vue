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
    },
  }),
  mounted () {
    console.log(this.$store.getters.solvedFunctionInformations)
  },
  methods: {
    click() {
      // const solvedFunctionInfo = this.$store.getters.solvedFunctionInformations;
      console.log(this.$store.getters.solvedFunctionInformations)
    }
  }
}
</script>
