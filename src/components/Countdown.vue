<template>
  <div
    class="base-timer"
    :style="{display: show ?'block':'none' }"
  >
    <div
      class="progress-marker green"
      :style="{width: `${progress}%`}"
    />
    <div class="time-left">{{formattedTimeLeft}}</div>
  </div>
</template>

<script>
export default {
  props: {
    defaultDuration: {
      type: Number,
      default: 20,
    },
    show: {
      type: Boolean,
      default: false,
    },
    interval: {
      type: Number,
      default: 1000
    }
  },
  data() {
    return {
      duration: 0,
      timePassed: 0,
      timerInterval: null,
    };
  },

  computed: {
    formattedTimeLeft() {
      const timeLeft = this.timeLeft;
      const minutes = Math.floor(timeLeft / 60);
      let seconds = Math.floor(timeLeft % 60);

      if (seconds < 10) {
        seconds = `0${seconds}`;
      }

      return `${minutes}:${seconds}`;
    },

    timeLeft() {
      return this.duration - this.timePassed;
    },

    timeFraction() {
      const rawTimeFraction = this.timeLeft / this.duration;
      return rawTimeFraction - (1 / this.duration) * (1 - rawTimeFraction);
    },

    progress() {
      const rawTimeFraction = (this.timeLeft * 100.0) / this.duration;
      return rawTimeFraction;
    },
  },

  watch: {
    timeLeft(newValue) {
      if (newValue <= 0) {
        console.log(" ????")
        this.onTimesUp();
      }
    },
  },

  mounted() {
    // this.startTimer();
  },

  methods: {
    onTimesUp() {
      clearInterval(this.timerInterval);
    },

    startTimer(newDuration) {
      clearInterval(this.timerInterval);
      this.duration = newDuration;
      this.timePassed = 0;
      this.timerInterval = setInterval(() => (this.timePassed += this.interval/1000.0), this.interval);
    },
  },
};
</script>

<style scoped lang="scss">
.base-timer {
  position: fixed;
  width: 100%;
  height: 3px;
  bottom: 0;
  left: 0;
  background: #e9e9e9;

  .progress-marker {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;

    &.green {
      background: rgb(65, 184, 131);
    }

    &.orange {
      background: orange;
    }

    &.red {
      background: red;
    }
  }

  .time-left {
    position: absolute;
    bottom: 5px;
    right: 5px;

    font-size: 0.75em;
    color: rgba(1, 1, 1, 0.2);
  }

  // &__label {
  //   position: absolute;
  //   width: 300px;
  //   height: 300px;
  //   top: 0;
  //   display: flex;
  //   align-items: center;
  //   justify-content: center;
  //   font-size: 48px;
  // }
}
</style>
