<template id="video-template">
  <video loop playsinline="" autoplay preload="auto">
    <source :src="src">
  </video>
</template>

<script>
export default {
  props: ["src"]
};
</script>