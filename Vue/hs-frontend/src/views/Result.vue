<template>
    <v-container fill-height>
      <v-row align="center">
        <v-col align="center">
          <v-btn @click="onClick()">test</v-btn>
          <Plotly :data="calculatedData" :layout="layout" :display-mode-bar="false"></Plotly>
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
      // title: "My graph"
    },
  }),
  mounted () {
    const solvedFunctionInfo = this.$store.getters.solvedFunctionInformations;
    const traceVariables = Object.keys(solvedFunctionInfo.trace);
    if(traceVariables.length == 2)
      this.data[0].x = solvedFunctionInfo.trace[traceVariables[0]];
      this.data[0].y = solvedFunctionInfo.trace[traceVariables[1]];
      // console.log(this.data.x)
  },
  methods: {
    onClick() {
      const solvedFunctionInfo = this.$store.getters.solvedFunctionInformations;
      const traceVariables = Object.keys(solvedFunctionInfo.trace);
      if(traceVariables.length == 2)
        this.data.x = solvedFunctionInfo.trace[traceVariables[0]];
        this.data.y = solvedFunctionInfo.trace[traceVariables[1]];
        console.log(this.data.x)
    }
  },
  computed: {
    calculatedData: function () {
      const solvedFunctionInfo = this.$store.getters.solvedFunctionInformations;
      const traceVariables = Object.keys(solvedFunctionInfo.trace);
      let data = [{
        x: null,
        y: null,
        type: "scatter"
      }, {
        z: [
          [10, 10.625, 12.5, 15.625, 20],
          [5.625, 6.25, 8.125, 11.25, 15.625],
          [2.5, 3.125, 5, 8.125, 12.5],
          [0.625, 1.25, 3.125, 6.25, 10.625],
          [0, 0.625, 2.5, 5.625, 10]
        ],
        x: [-9, -6, -5, -3, -1],
        y: [0, 1, 4, 5, 7],
        type: "contour"
      }];
      if(traceVariables.length == 2){
        data[0].x = solvedFunctionInfo.trace[traceVariables[0]];
        data[0].y = solvedFunctionInfo.trace[traceVariables[1]];

        const variablesBandwidth = this.$store.getters.variablesBandwidth;
        data[1].z = solvedFunctionInfo.Z;
        let linspace = require( 'compute-linspace' );
        data[1].x  = linspace( parseFloat(variablesBandwidth[0][0]), parseFloat(variablesBandwidth[0][1]), data[1].z.length);
        data[1].y = linspace( parseFloat(variablesBandwidth[1][0]), parseFloat(variablesBandwidth[1][1]), data[1].z[0].length);
        }
      return data;
    }
  }
}
</script>
