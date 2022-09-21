<template>
  <div class="section-wrapper row bg-light align-items-center justify-content-center flex-fill" v-if="loaded">
    <section class="block block__form">
      <h2>New VAL experiment</h2>
      <form class="text-left pt-5" v-on:submit.prevent="submitForm">
        <div class="form-group row">
          <label for="experimentId" class="col-sm-4">Experiment ID</label>
          <div class="col-sm-8">
            <input type="text" class="form-control" id="experimentId" aria-describedby="uidHelp" placeholder="Enter user ID" v-model="experimentSettings.experimentId">
            <small id="uidHelp" class="form-text text-muted">This ID is generated automatically, please do cross check.</small>
          </div>
        </div>

        <fieldset class="form-group">
          <div class="row">
            <legend class="col-form-label col-sm-4 pt-0">Drink preferences</legend>

            <div class="col-sm-8">
              <div class="form-check">
                <input type="radio" class="form-check-input" id="drink_1" value="beers" v-model="experimentSettings.drink_preferences">
                <label class="form-check-label" for="drink_1">Beers</label>
              </div>
              <div class="form-check">
                <input type="radio" class="form-check-input" id="drink_2" value="red_wine" v-model="experimentSettings.drink_preferences">
                <label class="form-check-label" for="drink_2">Red wine</label>
              </div>
              <div class="form-check">
                <input type="radio" class="form-check-input" id="drink_3" value="white_wine" v-model="experimentSettings.drink_preferences">
                <label class="form-check-label" for="drink_3">White wine</label>
              </div>
              <div class="form-check">
                <input type="radio" class="form-check-input" id="drink_4" value="mixed_wine" v-model="experimentSettings.drink_preferences">
                <label class="form-check-label" for="drink_4">Mixed wine</label>
              </div>
              <div class="form-check">
                <input type="radio" class="form-check-input" id="drink_5" value="mixed_wine_beers" v-model="experimentSettings.drink_preferences">
                <label class="form-check-label" for="drink_5">Mixed wine and beers</label>
              </div>
            </div>
          </div>
        </fieldset>

        <fieldset class="form-group">
          <div class="row">
            <legend class="col-form-label col-sm-4 pt-0">Language</legend>

            <div class="col-sm-8">
              <div class="form-check">
                <input type="radio" class="form-check-input" id="lang_1" value="EN" v-model="experimentSettings.language">
                <label class="form-check-label" for="lang_1">English</label>
              </div>

              <div class="form-check">
                <input type="radio" class="form-check-input" id="lang_2" value="NL" v-model="experimentSettings.language">
                <label class="form-check-label" for="lang_2">Nederlands</label>
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
  data() {
    return {
      loaded: false,
      experimentSettings: {
        experimentId: undefined,
        order: "CUE_MAT",
        language: "NL",
        drink_preferences: "mixed_wine_beers"
      },
    };
  },
  methods: {
    submitForm() {
      axios
        .post("/experiment/val/create", {
          order: this.experimentSettings.order,
          experiment_id: this.experimentSettings.experimentId,
          language: this.experimentSettings.language,
          drink_preferences: this.experimentSettings.drink_preferences
        })
        .then(({ data }) => {
          //Perform Success Action
          console.log("success -> go to next", data);
          if (data.isOk) {
            this.$router.push(`/experiment/val/${data.experimentId}`);
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
    axios.post("/experiment/val/request-new-id").then(({ data }) => {
      this.experimentSettings.experimentId = data.id;
      this.loaded = true;
    });
  },
};
</script>
