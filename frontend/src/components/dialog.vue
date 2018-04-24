<template>
  <div class="intro">
    <el-button class="headimage"
      :style="{backgroundImage: 'url(' + headimage + ')'}">
    </el-button>
    <div class="info">
      <h4><i class="el-icon-edit"></i> 郭性的分享和自言自语</h4>
      <p>Github: <a href="https://github.com/guoxingx">guoxingx</a></p>
      <p v-for="info in infos">{{ info }}</p>
    </div>
  </div>
</template>

<script type="text/javascript">
export default {
  props: ['headimage', 'infos']
}
</script>
