<template>
  <div>
    <el-popover
      ref="inputAddressBoard"
      placement="right"
      width="300"
      v-model="visible4">
      <el-row>
        <el-col :span="20">
          <el-input type="text" v-model="address" placeholder="输入已存在的账号地址"></el-input>
        </el-col>
        <el-col :span="3" :offset="1">
          <el-button type="Blue" icon="el-icon-check" @click="setAddress" circle></el-button>
        </el-col>
      </el-row>
    </el-popover>
  </div>
</template>
