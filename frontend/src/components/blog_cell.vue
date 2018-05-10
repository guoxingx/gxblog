<template>

  <div class="blog-unit">
    <div>
      <div style="float: left; margin-right: 30px;">
        <!-- <router-link :to="{ name: 'blog', params: { id: blog.id }}"> -->
        <router-link :to="{ name: 'blog', params: { id: blog.id }}">
          <img :src="blog.image">
        </router-link>
      </div>
      <div style="text-align: left;">
        <div>
          <!-- <router-link :to="{ name: 'blog', params: { id: blog.id }}"> -->
          <router-link :to="{ name: 'blog', params: { id: blog.id }}">
            <h3>{{ blog.title }}</h3>
          </router-link>
        </div>
        <div style="">
          <p>{{ blog.summary }}</p>
        </div>
        <div style="margin-bottom: 10px;">
          <el-tag class="tag" v-for="tag in blog.tags" :key="tag" type="success">{{ tag }}</el-tag>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  props: ['blog']
}
</script>

<style>
.blog-unit {
  display: inline-block;
  margin-top: 30px;
  width: 95%;
  /*height: 200px;*/
  /*max-height: 200px;*/

  padding-top: 20px;
  border-bottom: 0.5px solid #BACCE3;
}

.blog-unit img {
  margin: 0 auto;
  max-height: 200px;
  width: 300px;
  /*max-width: 100%;*/
  /*max-width: 800px;*/
  vertical-align: middle;
}

.blog-unit .tag {
  margin-bottom: 10px;
  margin-left: 10px;
}

.blog-unit a {
  text-decoration: none;
}

.blog-unit-left {
  float: left;
}
.blog-unit-text {
  text-align: left;
}

</style>
