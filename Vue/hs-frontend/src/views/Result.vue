<template>
    <v-container>
      <v-row justify="center">
        <v-card class="mt-5" >
          <v-card-title>
              Solution
          </v-card-title>
          <v-card-text>
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Function value: {{ functionValue }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Iterations: {{ iterations }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense v-for="varName in variablesNames" :key="varName">
              <v-list-item-content>
                <v-list-item-title>{{ varName }}: {{ optimalPiont[varName] }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-card-text>
        </v-card>
      </v-row>
      <div class="my-1">
        <Plotly 
          :data="calculatedData" 
          :layout="layout" 
          :display-mode-bar="true" 
          :scrollZoom="true"
          :responsive="true"
          >
        </Plotly>
      </div>
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
  
  }),
  computed: {
    calculatedData: function () {
      const solvedFunctionInfo = this.$store.getters.solvedFunctionInformations;
      const traceVariables = Object.keys(solvedFunctionInfo.trace);
      let data = [{
        x: null,
        y: null,
        type: "scatter"
      }, {
        z: null,
        x: null,
        y: null,
        type: "contour",
        contours: {
          showlabels: true,
          labelfont: {
            family: 'Raleway',
            size: 12,
            color: 'white',
          }
        }
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
    },
    functionValue: function () {
      return this.$store.getters.solvedFunctionInformations.functionValue;
    },
    iterations: function () {
      return this.$store.getters.solvedFunctionInformations.iterations;
    },
    variablesNames: function () {
      const optimalPiont = this.$store.getters.solvedFunctionInformations.optimalVariables;
      return Object.keys(optimalPiont);
    },
    optimalPiont: function () {
      return this.$store.getters.solvedFunctionInformations.optimalVariables;
    },
    layout: function () {
      const solvedFunctionInfo = this.$store.getters.solvedFunctionInformations;
      const traceVariables = Object.keys(solvedFunctionInfo.trace);
      let layout = {
        showlegend: false,
        margin: {
          l: 50,
          r: 30,
          b: 50,
          t: 30,
          pad: 4
        },
        xaxis: {title: {text: traceVariables[0]}},
        yaxis: {title: {text: traceVariables[1]}}
      }
      return layout;
    }
  }
}
</script>
