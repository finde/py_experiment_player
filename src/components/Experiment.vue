<template>
  <div v-if="currentStepIndex>=0" class="section-wrapper row bg-light align-items-center justify-content-center flex-fill">

    <div class="debug-info" v-if="enableDebugging">
      <ul>
        <li>isUsingTimer : {{isUsingTimer}} </li>
        <li>currentStepIndex : {{ currentStepIndex }}</li>
        <li>currentDisplay: {{ currentDisplay }}</li>
        <li v-if="currentDisplay != steps[currentStepIndex]">realStep: {{ steps[currentStepIndex] }}</li>
        <li>preconditions: {{ preconditionValue }}</li>
        <li>options: {{ options }}</li>
      </ul>
    </div>

    <section v-if="currentDisplay.type==='intro'">
      <div class="jumbotron">
        <h2 class="display-4">{{currentDisplay.title[options.language]}}</h2>        
      </div>
      <p class="lead">
        <button @click="goNext()" class="btn btn-primary mt-5 has-keyboard-alternative" v-html="button.continue[options.language]" />
      </p>
      <!-- <p>
        <button
          class="btn btn-light btn-small"
          @click="playSound()"
        >Test Sound</button>
      </p> -->
    </section>

    <section v-else-if="currentDisplay.type === 'preconditions'" class="block block__preconditions">
      <div v-for="(condition, condIndex) in currentDisplay.items" :key="`cond-${condIndex}`">
        <p>{{condition.text[options.language]}}</p>
        <template v-if="condition.type === 'checkboxes'">
          <div class="form-check form-check-inline" v-for="(opt, optIndex) in condition.options" :key="`opt-${optIndex}`">
            <input type="checkbox" class="form-check-input" :id="`opt-${condIndex}-${optIndex}`" :value="opt.key" v-model="preconditionValue[condition.id]">
            <label class="form-check-label" :for="`opt-${condIndex}-${optIndex}`">{{opt.text[options.language]}}</label>
          </div>
        </template>
        <template v-else-if="condition.type === 'radio_button'">
          <div class="form-check form-check-inline" v-for="(opt, optIndex) in condition.options" :key="`opt-${optIndex}`">
            <input type="radio" class="form-check-input" :id="`opt-${condIndex}-${optIndex}`" :value="opt.key" v-model="preconditionValue[condition.id]">
            <label class="form-check-label" :for="`opt-${condIndex}-${optIndex}`">{{opt.text[options.language]}}</label>
          </div>
        </template>
      </div>

      <button @click="goNext()" class="btn btn-primary mt-5 has-keyboard-alternative" v-html="button.continue[options.language]" />
    </section>

    <section v-else-if="currentDisplay.type === 'instruction'" class="block block__instruction">
      <img v-if="currentDisplay.icon" class="block__instruction__icon" :src="require(`@/assets/${currentDisplay.icon}`)" :width="currentDisplay.iconWidth" :height="currentDisplay.iconHeight" />
      <p class="block__instruction__text" v-html="currentDisplay.text[options.language]" />

      <dir v-if="!currentDisplay.duration" class="p-0">
        <button @click="goNext()" class="btn btn-primary mt-5 has-keyboard-alternative" v-html="button.continue[options.language]" />
      </dir>
    </section>

    <section v-else-if="currentDisplay.type === 'media'" class="block block__media">
      <video playsinline="" autoplay preload="auto">
        <source v-if="!currentDisplay.cond" :src="`/assets/${this.$route.params.exp_id}${currentDisplay.file}`">
        <source v-else :src="currentDisplay.condFile[options[currentDisplay.cond]]">
      </video>
    </section>

    <section v-else-if="currentDisplay.type === 'rating'" class="block block__rating">
      <p class="block__rating__text" v-html="currentDisplay.text[options.language]" />
      <div class="block__rating__options">
        <span class="block__rating__options__desc">{{currentDisplay.min_description[options.language]}}</span>

        <template v-if="currentDisplay.is_slider">
          <input class="block__rating__options__input" type="range" v-model="selectedRating" :min="currentDisplay.min" :max="currentDisplay.max">
        </template>
        <template v-if="!currentDisplay.is_slider">
          <div class="form-check square_options" v-for="value of createArray(currentDisplay.min, currentDisplay.max)" v-bind:key="value"
            :class="{first:currentDisplay.min==value, last:currentDisplay.max==value}">
            <input type="radio" class="form-check-input" :id="`rating_${value}`" :value="value" v-model="selectedRating">
            <label class="form-check-label" :class="{selected:selectedRating==value}" :for="`rating_${value}`">{{value}}</label>
          </div>          
        </template>

        <span class="block__rating__options__desc">{{currentDisplay.max_description[options.language]}}</span>
      </div>

      <button @click="submitAndNext()" class="btn btn-primary mt-5 has-keyboard-alternative" v-html="button.continue[options.language]" />
    </section>

    <section v-else-if="currentDisplay.type === 'composite-rating' && currentDisplay.items.length > 0" 
             class="block block__composite-rating">
      <div class="row" >
        <div v-if="currentDisplay.items[subsectionIndex].endsWith('.jpg') || currentDisplay.items[subsectionIndex].endsWith('.png')"
              class="col col-6 block__composite-rating__item" 
              :key="`img-${subsectionIndex}`"
              :style="{backgroundImage: `url('${currentDisplay.items[subsectionIndex]}')`}">
        </div>
        <div v-else-if="currentDisplay.items[subsectionIndex].endsWith('.mp4')" class="col col-6 block__composite-rating__item">
          <video-slide :src="currentDisplay.items[subsectionIndex]" :key="`vid-${subsectionIndex}`"/>
        </div>

        <div class="col col-6 block__composite-rating__questions">
          <div class="block__composite-rating__question" v-for="(question, qIndex) in currentDisplay.questions" :key="`question-${qIndex}`">
            <p class="block__rating__text"  v-html="question.text[options.language]" />
            <div class="block__rating__options">
              <span class="block__rating__options__desc">{{question.min_description[options.language]}}</span>
              <input type="range" :min="+question.min" :max="+question.max" class="block__rating__options__input" v-model="selectedCompositeRating[`${subsectionIndex}_${qIndex}`]">
              <span class="block__rating__options__desc">{{question.max_description[options.language]}}</span>
            </div>
          </div>
        
          <button @click="submitAndNext()" class="btn btn-primary mt-5 has-keyboard-alternative" v-html="button.continue[options.language]" />
        </div>
      </div>
    </section>

    <!-- IMAGE SLIDE SHOW -->
    <section v-else-if="currentDisplay.type === 'slideshow'" class="block block__slideshow">
      
      <template v-if="currentDisplay.items.length > 0">
        <div class="block__slideshow__item" :style="{backgroundImage: `url('${currentDisplay.items[subsectionIndex]}')`}" />
      </template>
      <template v-else-if="!!currentDisplay.cond">
        <div class="block__slideshow__item" :style="{backgroundImage: `url('${currentDisplay.condItems[options[currentDisplay.cond]][subsectionIndex]}')`}" />
      </template>
      <template v-else>
        <div class="block__slideshow__item" :style="{backgroundImage: `url('${currentDisplay.getItems(options)[subsectionIndex]}')`}" />
      </template>
    </section>
    <section v-else-if="currentDisplay.type === 'playlist'" class="block block__playlist">
      <vue-playlist :playlist="currentDisplay.getItems(options)" :autostart="true"></vue-playlist>
    </section>
    <section v-else-if="currentDisplay.type === 'quiz'" class="block block__quiz">
      <p class="mb-5" v-if="isQuizAnswer !== ''"><b>Score : {{quizScore}}</b></p>
      <p class="mb-5" v-else>Score : {{quizScore}}</p>

      <font-awesome-icon icon="times" size="4x" v-if="isQuizAnswer == 'wrong'" :style="{ color: 'red' }" />
      <font-awesome-icon icon="check" size="4x" v-else-if="isQuizAnswer == 'correct'" :style="{ color: 'green' }" />
      <form v-else @submit.prevent="onQuizAnswer()">
        <p class="form-group"><b>{{currentDisplay.items[subsectionIndex].question}}</b></p>
        <div class="form-group">
          <input type="text" ref="needToFocus" v-model="answerField">
        </div>

        <countdown :show="true" class="subtimer" :duration="currentDisplay.durationPerItem / 1000.0" :interval="100" ref="subtimer" />

        <p class="small">Press [Enter] to submit answer</p>
      </form>
      <!-- {{currentDisplay.items[subsectionIndex].answer}} -->
    </section>
    <section v-else-if="currentDisplay.type === 'closing'" class="block block__instruction">
      <p class="block__instruction__text" v-html="currentDisplay.text[options.language]" />
    </section>
    <countdown :show="isUsingTimer && !!currentDisplay.duration" :duration="currentDisplay.duration / 1000.0" ref="timer" />
  </div>
</template>

<script>
import { Experiment } from "./Experiment.js";
import Countdown from "@/components/Countdown";
import VideoSlide from "@/components/VideoSlide";
import VuePlaylist from "@/components/VuePlaylist";
import "bootstrap/dist/css/bootstrap.css";
import axios from "axios";

// FIXME :: set to -1 for production
let currentStepIndex = -1;

export default {
  name: "Experiment",
  components: {
    Countdown,
    VuePlaylist,
    VideoSlide
  },
  props: {
    jsonData: Object,
    isUsingTimerAsDefault: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    // const self = this;
    //Define Parse JSON to Experiment Object
    const experiment = new Experiment(this.jsonData);

    console.log(experiment);
    const steps = experiment.flattenItem;
    const currentDisplay = steps[currentStepIndex];

    return {
      experiment,
      steps,
      currentDisplay,
      currentStepIndex,
      // isUsingTimer: false,
      enableDebugging: false,
      selectedRating: 5,
      selectedCompositeRating: [],
      timer: undefined,
      interval: undefined,
      subtimer: undefined,
      subsectionIndex: 0,
      isUsingTimer: this.isUsingTimerAsDefault,
      preconditionValue: {},
      options: {
        drink_preferences: this.jsonData.drink_preferences,
        language: this.jsonData.language,
      },
      answerField: "",
      isQuizAnswer: "",
      quizScore: 0,
      button: {
        continue: {
          en: `Continue<span class="keyboard-info">or press <b>ENTER</b></span>`,
          nl: `Volgende<span class="keyboard-info">of druk op <b>ENTER</b> om door te gaan</span>`,
        },
      },
    };
  },
  methods: {
    createArray(minNum, maxNum) {
      var list = [];
      for (var i = minNum; i <= maxNum; i++) {
          list.push(i);
      }
      return list
    },
    sectionInit(nextStep) {
      const self = this;

      // reset temporal based variable
      self.subsectionIndex = 0;
      self.answerField = "";
      clearTimeout(self.timer);
      clearInterval(self.interval);
      clearTimeout(self.subtimer);

      console.log(
        "SECTION INIT",
        `showing ${self.steps[self.currentStepIndex].type}-${
          self.currentStepIndex
        } for ${self.steps[self.currentStepIndex].duration || "?"}secs`
      );

      // special cases init

      // if visual, update display
      if (nextStep.isVisual) {
        self.currentDisplay = nextStep;

        if (nextStep.duration > 0)
          self.$refs.timer.startTimer(nextStep.duration / 1000.0);

        switch (nextStep.type) {
          // if precondition, reset
          case "preconditions":
            nextStep.items.forEach(({ id, type, defaultValue }) => {
              if (type === "checkboxes") {
                this.$set(self.preconditionValue, id, defaultValue || []);
              } else {
                this.$set(
                  self.preconditionValue,
                  id,
                  defaultValue || undefined
                );
              }
            });
            break;

          // if slideshow, set interval for updating subsectionIndex
          case "slideshow":
            self.interval = setInterval(() => {
              self.subsectionIndex++;
            }, nextStep.durationPerItem || 1000);
            break;

          // set the first quiz
          case "quiz":
            setTimeout(() => {
              self.$refs.subtimer.startTimer(
                self.currentDisplay.durationPerItem / 1000.0
              );
              if (self.$refs.needToFocus) self.$refs.needToFocus.focus();

              self.subtimer = setTimeout(() => {
                self.onQuizAnswer();
              }, self.currentDisplay.durationPerItem);
            }, 1);

            break;

          case "rating":
            self.selectedRating = Math.ceil((self.currentDisplay.min + self.currentDisplay.max) * 0.5)
            break;

          case "composite-rating":
            self.subsectionIndex = 0
            self.selectedCompositeRating = {}
            for (let i=0; i<nextStep.items.length; i++) {
              for (let j=0; j<nextStep.questions.length; j++) {
                self.selectedCompositeRating[`${i}_${j}`] = (nextStep.questions[j].max + nextStep.questions[j].min) * 0.5
              }
            }
            break;

          default:
            console.log(`${nextStep.type} doesn't need pre-setting`);
        }
      } else {
        // if not visual, keep the current display
        switch (nextStep.type) {
          case "media":
            if (
              nextStep.file.endsWith(".wav") ||
              nextStep.file.endsWith(".mp3")
            ) {
              self.playSound(nextStep.file, nextStep.volume);
            }
            break;
          case "marker":
            axios.get(`/experiment/${this.$route.params.exp_id}/marker/${nextStep.code}`);
            break;
          case "delay":
            // Delay is doing nothing
            break;
          default:
            console.warn(`[${nextStep.type}] is not handled`);
            break;
        }
      }

      if (self.$refs.needToFocus) self.$refs.needToFocus.focus();
    },
    playSound(mediaFile = "beep-02.mp3", volume = 1.0) {
      var audio = new Audio(require(`@/assets/${mediaFile}`));
      audio.volume = volume;
      const playPromise = audio.play();

      // In browsers that don't yet support this functionality,
      // playPromise won't be defined.
      if (playPromise !== undefined) {
        playPromise
          .then(function () {
            // Automatic playback started!
          })
          .catch(function (error) {
            // Automatic playback failed.
            // Show a UI element to let the user manually start playback.
            console.error(" >> ", error, audio);
          });
      }
    },
    goNext() {
      const self = this;

      if (self.currentStepIndex == self.steps.length - 1) {
        console.log("last block");
        return
      }
      
      console.log("continue");
      
      /* eslint-disable no-debugger */
      // debugger;
      /* eslint-enable  no-debugger */

      // before update step
      if (self.currentStepIndex >= 0) {
        const currentStep = self.steps[self.currentStepIndex];
        if (currentStep.type === "preconditions") {
          console.log(currentStep, self.preconditionValue);

          currentStep.items.forEach(({ id }) => {
            self.options[id] = self.preconditionValue[id];
          });
        }
      }

      // update step
      if (self.currentStepIndex < self.steps.length) {
        const nextStep = self.steps[++self.currentStepIndex];

        // after update step
        self.isUsingTimer = true;
        self.sectionInit(nextStep);

        // show timer if isUsingTimer and content is Visual and has duration
        if (self.isUsingTimer) {
          let duration = self.steps[self.currentStepIndex].isVisual
            ? self.steps[self.currentStepIndex].duration
            : 1;

          // delay is special case
          if (nextStep.type == "delay") {
            duration = self.steps[self.currentStepIndex].duration;
          }

          if (duration) {
            self.$refs.timer.startTimer(
              self.steps[self.currentStepIndex].duration / 1000.0
            );
            self.timer = setTimeout(() => {
              self.goNext();
            }, self.steps[self.currentStepIndex].duration || 1);
          }
        }
      }
    },
    goPrev() {
      if (this.currentStepIndex <= 0) {
        return;
      }

      this.sectionInit();

      const prevStep = this.steps[--this.currentStepIndex];
      this.isUsingTimer = false;
      if (prevStep.isVisual) {
        this.currentDisplay = prevStep;
      }
    },
    submitAndNext() {
      if (this.currentDisplay.type == 'rating') {
        axios
          .post(`/experiment/${this.$route.params.exp_id}/rating-answer`, {
            experiment_id: this.$route.params.id,
            block_name: "" + this.currentDisplay.block_name,
            name: "" + this.currentDisplay.name,
            value: +this.selectedRating,
          })
          .then(() => {
            this.goNext();
          })
          .catch((error) => {
            console.error("error :::  ", error);
          });
      } else if (this.currentDisplay.type == 'composite-rating') {
        if (this.subsectionIndex < this.currentDisplay.items.length-2) {
          this.subsectionIndex++;
        } else {
          let sanitizedValue = {}
          Object.keys(this.selectedCompositeRating).map((k) => {
            sanitizedValue[k] = +this.selectedCompositeRating[k]
          })
          console.log(this.$route.params)
          axios
          .post(`/experiment/${this.$route.params.exp_id}/composite-rating-answer`, {
            experiment_id: this.$route.params.id,
            block_name: "" + this.currentDisplay.block_name,
            name: "" + this.currentDisplay.name,
            value: sanitizedValue,
          })
          .then(() => {
            this.goNext();
          })
          .catch((error) => {
            console.error("error :::  ", error);
          });
        }
      }
    },
    _keyDownListener(e) {
      if (this.enableDebugging) {
        if (e.key === "ArrowRight") {
          this.goNext();
          e.preventDefault();
        } else if (e.key === "ArrowLeft") {
          this.goPrev();
          e.preventDefault();
        }
      }

      if ((e.ctrlKey || e.metaKey) && !this.ctrlKeyOn) {
        this.ctrlKeyOn = true;
      }

      if (this.ctrlKeyOn && e.key === "d") {
        e.preventDefault(); //prevent the default action (save page in this case)
        this.enableDebugging = !this.enableDebugging;
      } else if (e.key === "Enter") {
        // if the currentStep is waiting for Continue
        if (!this.currentDisplay.duration) {
          e.preventDefault();

          // if VASS, then submit
          if (this.currentDisplay.type === 'rating') {
            this.submitAndNext();
          } else {
            this.goNext();
          }
        }
      }
    },
    _keyUpListener(e) {
      if ((e.ctrlKey || e.metaKey) && this.ctrlKeyOn) {
        this.ctrlKeyOn = false;
      }
    },
    onQuizAnswer() {
      const self = this;

      clearTimeout(self.subtimer);

      console.log(
        this.answerField,
        this.currentDisplay.items[this.subsectionIndex].answer
      );

      if (
        this.currentDisplay.items[this.subsectionIndex].answer ===
        +this.answerField
      ) {
        this.isQuizAnswer = "correct";
        if (!this.currentDisplay.isTutorial) {
          this.quizScore++;
          this.playSound("correct_buzzer.mp3");
        }
      } else {
        this.isQuizAnswer = "wrong";
        if (!this.currentDisplay.isTutorial) {
          this.quizScore--;
          this.playSound("wrong_buzzer.mp3");
        }
      }

      setTimeout(() => {
        self.isQuizAnswer = "";
        self.answerField = "";
        self.subsectionIndex++;

        // reset the countdown
        setTimeout(() => {
          self.$refs.subtimer.startTimer(
            self.currentDisplay.durationPerItem / 1000.0
          );
          if (self.$refs.needToFocus) self.$refs.needToFocus.focus();
        }, 1);

        // on subtimer timeout, auto Continue
        self.subtimer = setTimeout(() => {
          self.onQuizAnswer();
        }, self.currentDisplay.durationPerItem);
      }, 800);
    },
  },
  mounted() {
    window.addEventListener("keydown", this._keyDownListener);
    window.addEventListener("keyup", this._keyUpListener);
    this.goNext();
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this._keyDownListener);
    window.removeEventListener("keyup", this._keyUpListener);
  },
};

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.section-wrapper {
  // background: url('~@/assets/bg.jpg');
  background: #fdfdfd;
}
.debug-info {
  position: absolute;
  top: 1em;
  left: 1em;
  text-align: left;
  font-size: 8px;
}
</style>
