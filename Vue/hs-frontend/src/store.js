import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    solvedFunctionInformations: null,
    variablesBandwidth: null
  },
  getters: {
    solvedFunctionInformations: state => {
      return state.solvedFunctionInformations
    },
    variablesBandwidth: state => {
      return state.variablesBandwidth
    }
  },
  mutations: {
    setFunctionInformations(state, solvedInfo) {
      state.solvedFunctionInformations = solvedInfo
    },
    setVariablesBandwidth(state, variablesBandwidth) {
      state.variablesBandwidth = variablesBandwidth
    }
  },
  actions: {}
 });