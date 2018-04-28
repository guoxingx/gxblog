<template>
  <div class="account-board">
    <div v-if="account">
      <el-button v-popover:showAccount>你的余额 {{ balance }} finny ({{ balance / 1000 }} ether)</el-button>
      <el-popover
        ref="showAccount"
        placement="right"
        width="330"
        trigger="click">
        <p><strong>{{ account }}</strong></p>
        <p>这是你的账户地址！</p>
        <el-button size="small" type="warning" @click="requestEth" round>给我一个以太币！</el-button>
      </el-popover>
    </div>
    <div v-if="!account">
      <el-button v-popover:registerBoard>注册账号！</el-button>

      <el-popover
        ref="registerBoard"
        placement="right"
        width="300"
        v-model="visible2">
        <el-row>
          <el-col :span="20">
            <el-input type="password" v-model="password" placeholder="输入密码来创建以太坊账号"></el-input>
          </el-col>
          <el-col :span="3" :offset="1">
            <el-button type="Blue" icon="el-icon-check" @click="register" circle></el-button>
          </el-col>
        </el-row>
      </el-popover>

    </div>
  </div>
</template>

<script>
import { getAccount } from '../account.js'
import { getBalance, registerAccount } from '../requests.js'

export default {
  data: {
    balance: 0,
    account: null
  },
  methods: {
    register () {
      registerAccount(this.password)
    },
    requestEth () {
      this.$message({
        message: '注意：等交易写入区块才能到账，约几十秒。自行刷新页面:)。前往www.bilibili.com查看进展。',
        showClose: true,
        type: 'warning',
        duration: 30000
      })
    }
  },
  created () {
    this.account = getAccount()
    getBalance
  }
}
</script>
