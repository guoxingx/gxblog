<template>

  <div class="unit">
    <div>
      <div style="float: left; margin-right: 30px;">
        <router-link :to="{ name: 'blog', params: { id: unit.id }}">
          <img :src="unit.image">
        </router-link>
      </div>
      <div style="text-align: left;">
        <div>
          <router-link :to="{ name: 'blog', params: { id: unit.id }}">
            <h3>{{ unit.title }}</h3>
          </router-link>
        </div>
        <div style="">
          <p>{{ unit.summary }}</p>
        </div>
        <div style="margin-bottom: 10px;">
          <el-tag class="tag" v-for="tag in unit.tags" :key="tag" type="success">{{ tag }}</el-tag>
        </div>
      </div>
    </div>

<!--     <el-row>
      <el-col :xs="0" :sm="8" :md="12" :lg="8" :xl="8">
        <router-link :to="{ name: 'blog', params: { id: unit.id }}">
          <img :src="unit.image">
        </router-link>
      </el-col>
      <el-col :xs="24" :sm="16" :md="12" :lg="16" :xl="16" class="unit-text">
        <el-row>
          <router-link :to="{ name: 'blog', params: { id: unit.id }}">
            <h3>{{ unit.title }}</h3>
          </router-link>
        </el-row>
        <el-row>
          <p>{{ unit.summary }}</p>
        </el-row>
        <el-row class="tags">
          <el-tag class="tag" v-for="tag in unit.tags" :key="tag" type="success">{{ tag }}</el-tag>
        </el-row>
      </el-col>
    </el-row> -->
  </div>

</template>

<script>
export default {
  props: ['unit']
}
</script>

<style>
.unit {
  display: inline-block;
  margin-top: 30px;
  width: 95%;
  /*height: 200px;*/
  /*max-height: 200px;*/

  padding-top: 20px;
  border-bottom: 0.5px solid #BACCE3;
}

.unit img {
  margin: 0 auto;
  max-height: 200px;
  width: 300px;
  /*max-width: 100%;*/
  /*max-width: 800px;*/
  vertical-align: middle;
}

.unit .tag {
  margin-bottom: 10px;
  margin-left: 10px;
}

.unit a {
  text-decoration: none;
}

.unit-left {
  float: left;
}
.unit-text {
  text-align: left;
}

</style>
