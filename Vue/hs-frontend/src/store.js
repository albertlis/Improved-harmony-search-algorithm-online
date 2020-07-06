import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    solvedFunctionInformations: null,
  },
  getters: {
    solvedFunctionInformations: state => {
      return state.solvedFunctionInformations
    }
  },
  mutations: {
    setFunctionInformations(state, solvedInfo) {
      state.solvedFunctionInformations = solvedInfo
    }
  },
  actions: {}
 });