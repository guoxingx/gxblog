<template>

  <div class="unit">
    <el-row>
      <el-col :xs="24" :sm="8" :md="6" :lg="5" :xl="4">
        <router-link :to="{ name: 'blog', params: { id: unit.id }}">
          <img :src="unit.image">
        </router-link>
      </el-col>
      <el-col :xs="24" :sm="16" :md="18" :lg="19" :xl="20">
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
    </el-row>
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
  height: 200px;
  max-height: 200px;

  padding-top: 20px;
  border-bottom: 0.5px solid #BACCE3;
}

.unit img {
  margin: 0 auto;
  max-height: 200px;
  max-width: 100%;
  vertical-align: middle;
}

.unit .tag {
  margin-bottom: 10px;
  margin-left: 10px;
}

.unit a {
  text-decoration: none;
}
</style>
