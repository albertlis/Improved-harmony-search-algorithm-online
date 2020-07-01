<template>
  <div class="text-center">
    <v-dialog
      v-model="dialog"
      max-width="800px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          light
          v-bind="attrs"
          v-on="on"
          x-large
          min-width="150"
        >
          Start
        </v-btn>
      </template>

      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          Set parameters
        </v-card-title>

        <v-card-text>
          <v-form class="px-3">
            <v-text-field label="Function" v-model="func" prepend-icon="functions" required> </v-text-field>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn color="primary" text @click="clearFunctionField">Clear</v-btn>
          <v-btn color="primary" text @click="dialog = false">
            Next
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      func: '',
      dialog: false,
    }
  },
  methods: {
    clearFunctionField: function () {
      this.func = ''
    }
  }
}
</script>