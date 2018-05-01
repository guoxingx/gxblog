<template>
  <el-card class="cell">
    <router-link :to="{ name: 'betonether', params: { id: boe.id }}">
      <div>
        <h4><span>{{ boe.home }}</span> vs <span>{{ boe.visiting }}</span></h4>
      </div>
    </router-link>
    <div>
      <p>{{ boe.opening_time }}</p>
      <router-link :to="{ name: 'betonether', params: { id: boe.id }}">
        <el-tag :type="boe.ended ? 'warning':'blue'" size="small">{{ boe.ended ? '已结束':'进行中' }}</el-tag>
      </router-link>
    </div>
  </el-card>
</template>

<script>
export default {
  props: ['boe']
}
</script>
