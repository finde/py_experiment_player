<template>
  <div class="section-wrapper row bg-light align-items-center justify-content-center flex-fill" v-if="is_loaded">
    <section class="block block__form">
        <div class="row justify-content-center">
          Available experiments:
        </div>
        <div class="row justify-content-center m-2" v-for="experiment_id in available_experiments" v-bind:key="experiment_id">
          <a style="max-width:240px;" :href="`/experiment/${experiment_id}`" type="button" class="btn btn-block btn-lg btn-primary">{{experiment_id}}</a>
        </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  methods: {
  },
  data() {
    return {
      is_loading: true,
      is_loaded: false,
      available_experiments: []
    }
  },
  mounted() {
    const self = this

    self.is_loading = true
    self.is_loaded = false
    // get list of experiment
    axios.get('/experiments_list')
    .then((res)=> {
      self.available_experiments = res.data['experiments']
      self.is_loaded = true
      self.is_loading = false
    })
  },
};
</script>
