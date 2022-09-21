<template>
  <div class="section-wrapper row bg-light align-items-center justify-content-center flex-fill" v-if="loaded">
    <section class="block block__form">
      <h2>New experiment</h2>
      <form class="text-left pt-5" v-on:submit.prevent="submitForm">
        <div class="form-group row">
          <label for="experiment_id" class="col-sm-4">Experiment ID</label>
          <div class="col-sm-8">
            <input type="text" class="form-control" id="experiment_id" aria-describedby="uidHelp" placeholder="Enter user ID" v-model="experimentSettings.experiment_id">
            <small id="uidHelp" class="form-text text-muted">This ID is generated automatically, please do cross check.</small>
          </div>
        </div>

        <fieldset class="form-group" v-for="formField of experimentSettingsSchema" v-bind:key="formField.id">
          <div class="row">
            <legend class="col-form-label col-sm-4 pt-0">{{formField.label}}</legend>

            <div v-if="formField.type==='choices'" class="col-sm-8">
              <div class="form-check" v-for="(option, index) of formField.options" v-bind:key="index">
                <input type="radio" class="form-check-input" :id="`${formField.id}_${index}`" :value="option.value" v-model="experimentSettings[formField.id]">
                <label class="form-check-label" :for="`${formField.id}_${index}`">{{option.label}}</label>
              </div>
            </div>

            <div v-if="formField.type==='boolean'" class="col-sm-8">
              <div class="form-check">
                <input type="checkbox" class="form-check-input" :id="`${formField.id}`" v-model="experimentSettings[formField.id]">
              </div>
            </div>

          </div>
        </fieldset>
      
        <div class="text-right">
          <button type="submit" class="btn btn-primary">Start Experiment</button>
        </div>
      </form>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  props: ["exp_id", "id"],
  data() {
    return {
      loaded: false,
      experimentSettingsSchema: [],
      experimentSettings: {
        experiment_id: undefined
      },
    };
  },
  methods: {
    submitForm() {
      let formData = new FormData()
      for (let [key, val] of Object.entries(this.experimentSettings)) {
        formData.append(key, val);
      }

      axios
        .post(`/experiment/${this.exp_id}/create`, formData)
        .then(({ data }) => {
          //Perform Success Action
          console.log("success -> go to next", data);
          if (data.isOk) {
            this.$router.push(`/experiment/${this.exp_id}/${data.experiment_id}`);
          }
        })
        .catch(() => {
          // error.response.status Check status code
          console.log("show error message: incorrect parameter");
        })
        .finally(() => {
          //Perform action in always
        });
    },
  },
  mounted() {
    axios.post(`/experiment/${this.exp_id}/get-config`)
      .then(({ data }) => {
        console.log(data)
        this.experimentSettingsSchema = data.forms
        if (data.forms) {
          for (let field of data.forms) {
            this.experimentSettings[field.id] = field.default
          }
        }

        axios.post(`/experiment/${this.exp_id}/request-new-id`)
        .then(({ data }) => {
          this.experimentSettings.experiment_id = data.id;
          this.loaded = true;
        });        
      })
  },
};
</script>
