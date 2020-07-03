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
          <v-form class="px-3" ref="form">
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
              label="HMS"
              :error-messages="HMSErrors"
              @change="$v.HMS.$touch()"
              @blur="$v.HMS.$touch()">
            </v-text-field>
            <v-row class="my-4">
              <v-range-slider
                v-model="HCMRRange"
                thumb-label="always"
                min=0
                max=1
                step=0.01
                thumb-size=28
                label="HCMR">
              </v-range-slider>
            </v-row>
            <v-row class="my-2">
              <v-range-slider
                v-model="PARRange"
                thumb-label="always"
                min=0
                max=1
                step=0.01
                thumb-size=28
                label="PAR">
              </v-range-slider>
            </v-row>
            <v-row>
              <v-text-field 
                v-model="bwMinValue"
                type="number"
                label="Bw min"
                :error-messages="bwMinErrors"
                @change="$v.bwMinValue.$touch()"
                @blur="$v.bwMinValue.$touch()">
              </v-text-field>
              <v-spacer></v-spacer>
              <v-text-field 
                v-model="bwMaxValue"
                type="number"
                label="Bw max"
                :error-messages="bwMaxErrors"
                @change="$v.bwMaxValue.$touch()"
                @blur="$v.bwMaxValue.$touch()">
              </v-text-field>
            </v-row>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn color="primary" text @click="clearForm">Clear</v-btn>
          <v-btn color="primary" text @click="goNext">Next</v-btn>
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
import { required, minValue, integer } from 'vuelidate/lib/validators'
export default {
  data() {
    return {
      func: '',
      dialog: false,
      valid: true,
      numberOfIterations: 1000,
      HMS: 10,
      HCMRRange: [0.5, 0.75],
      PARRange: [0.2, 0.8],
      bwMinValue: 1.0,
      bwMaxValue: 2.0,
      submitStatus: null
    }
  },
  methods: {
    clearForm: function () {
      this.$refs.form.reset();
      this.HMS = 10;
      this.numberOfIterations = 1000;
      this.HCMRRange = [0.5, 0.75];
      this.PARRange = [0.5, 0.75];
      this.bwMinValue = 1.0;
      this.bwMaxValue = 2.0;
    },
    getBwMaxValue: function () {
      return this.bwMaxValue;
    },
    goNext: function () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        this.submitStatus = 'ERROR'
      } else {
        // do your submit logic here
        this.submitStatus = 'PENDING'
        setTimeout(() => {
          this.submitStatus = 'OK'
        }, 500)
      }
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
    },
    bwMinValue: {
      required,
      minValue: minValue(0),
    },
    bwMaxValue: {
      required,
      minValue: minValue(0),
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
    },
    bwMinErrors () {
      const errors = []
      if (!this.$v.bwMinValue.$dirty) return errors
        !this.$v.bwMinValue.required && errors.push('Bw min  is required.')
        !this.$v.bwMinValue.minValue && errors.push('Bw min  have to be more than 0')
        if(this.bwMinValue >= this.bwMaxValue)
          errors.push('Bw min have to be less than Bw max')
        return errors
    },
    bwMaxErrors () {
      const errors = []
      if (!this.$v.bwMaxValue.$dirty) return errors
        !this.$v.bwMaxValue.required && errors.push('bwMax is required.')
        !this.$v.bwMaxValue.minValue && errors.push('bwMax have to be more than 0')
        if(this.bwMinValue >= this.bwMaxValue)
          errors.push('Bw max have to be more than Bw min')
        return errors
    }
  }
}
</script>