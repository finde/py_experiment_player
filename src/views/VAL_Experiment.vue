<template>
  <experiment v-if="is_loaded" :json-data="jsonData" />
</template>

<script>
import axios from "axios";
import Experiment from "@/components/Experiment.vue";
// import jsonData from "@/assets/experiment_settings/sad_v1";

export default {
  name: "ExperimentView",
  components: {
    Experiment,
  },
  props: ["exp_id", "id"],
  data() {
    return {
      jsonData: {},
      is_loaded: false,
    };
  },
  mounted() {
    const self = this
    axios
      .post(`/experiment/val/${this.id}`)
      .then(function ({ data }) {
        console.log(data);
        self.jsonData = data;
        self.is_loaded = true;
      })
      .catch(function (error) {
        console.log(error);
      });
  },
};
</script>

<style lang="scss">
</style>