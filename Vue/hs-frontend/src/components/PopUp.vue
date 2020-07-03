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
          <v-form class="px-3" ref="form" lazy-validation>
            <v-text-field label="Function" 
              v-model="func" 
              prepend-icon="functions" 
              :error-messages="funcErrors"
              @input="$v.func.$touch()"
              @blur="$v.func.$touch()"> 
            </v-text-field>
            <v-text-field 
              v-model="numberOfIterations"
              type="number"
              label="Interations"
              :error-messages="iterationsErrors"
              @change="$v.numberOfIterations.$touch()"
              @blur="$v.numberOfIterations.$touch()">
            </v-text-field>
            <v-text-field 
              v-model="HMS"
              type="number"
              label="Interations"
              :error-messages="HMSErrors"
              @change="$v.HMS.$touch()"
              @blur="$v.HMS.$touch()">
            </v-text-field>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn color="primary" text @click="clearForm">Clear</v-btn>
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
import { validationMixin } from 'vuelidate'
import { required, minValue, integer } from 'vuelidate/lib/validators'
export default {
  mixins: [validationMixin],

  data() {
    return {
      func: '',
      dialog: false,
      valid: true,
      numberOfIterations: 1000,
      HMS: 10,
    }
  },
  methods: {
    clearForm: function () {
      this.$refs.form.reset()
    }
  },
  validations: {
    func: {required},
    numberOfIterations : {
      required,
      minValue: minValue(1),
      integer,
    },
    HMS: {
      required,
      minValue: minValue(1),
      integer,
    }
  },
  computed: { 
    funcErrors () {
      const errors = []
      if (!this.$v.func.$dirty) return errors
        !this.$v.func.required && errors.push('Function is required.')
        return errors
    },
    iterationsErrors () {
      const errors = []
      if (!this.$v.numberOfIterations.$dirty) return errors
        !this.$v.numberOfIterations.required && errors.push('Iterations is required.')
        !this.$v.numberOfIterations.minValue && errors.push('Iterations have to be more than 0')
        !this.$v.numberOfIterations.integer && errors.push('Iterations have to be integer value')
        return errors
    },
    HMSErrors () {
      const errors = []
      if (!this.$v.HMS.$dirty) return errors
        !this.$v.HMS.required && errors.push('HMS is required.')
        !this.$v.HMS.minValue && errors.push('HMS have to be more than 0')
        !this.$v.HMS.integer && errors.push('HMS have to be integer value')
        return errors
    }
  }
}
</script>