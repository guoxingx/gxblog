<template>
  <div>
    <div v-if="account">
      <el-button v-popover:showAccount>你的余额 {{ balance }} finny ({{ balance / 1000 }} ether)</el-button>
      <el-popover
        ref="showAccount"
        placement="right"
        width="330"
        v-model="visible2"
        trigger="click">
        <p><strong>{{ account }}</strong></p>
        <p>这是你的账户地址</p>
        <el-button size="small" type="warning" @click="requestEth" round>给我一个以太币！</el-button>
        <el-button size="small" type="danger" @click="unsetAccount" round>登出账号</el-button>
      </el-popover>
    </div>
    <div v-if="!account">
      <el-button v-popover:inputAddressBoard>输入账号</el-button>
      <el-button v-popover:registerBoard>注册账号！</el-button>

      <el-popover
        ref="registerBoard"
        placement="right"
        width="300"
        v-model="visible3">
        <el-row>
          <el-col :span="20">
            <el-input type="password" v-model="password" placeholder="输入密码来创建以太坊账号"></el-input>
          </el-col>
          <el-col :span="3" :offset="1">
            <el-button type="Blue" icon="el-icon-check" @click="register" circle></el-button>
          </el-col>
        </el-row>
      </el-popover>

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

  </div>
</template>

<script>
import { setAccount, logoutAccount } from '@/js/account.js'
import { getBalance, registerAccount, requestTestEther } from '@/js/requests.js'

export default {
  props: ['balance', 'account', 'nodeStatus'],
  data () {
    return {
      // balance: 0,
      // account: null,
      visible2: false,
      visible3: false,
      visible4: false
    }
  },
  methods: {
    setAddress () {
      this.account = this.address
      setAccount(this.address)
      getBalance(this.address).then(res => {
        if (res.status === 200 && res.data.code === 0) {
          this.balance = Math.round(res.data.data / 1000000000000000)
        }
        this.visible2 = false
        this.visible4 = false
      })
    },
    unsetAccount () {
      this.account = null
      logoutAccount()
      this.visible2 = false
      this.visible4 = false
    },
    register () {
      registerAccount(this.password).then(res => {
        if (res.status === 200 && res.data.code === 0) {
          var data = res.data.data
          this.account = data
          setAccount(data)
          this.visible3 = false
          this.balance = 0
        }
      })
    },
    requestEth () {
      if (this.nodeStatus === 0) {
        requestTestEther(this.account).then(res => {
          if (res.data.amount || res.data.code === 0) {
            this.$message({
              message: '请求成功！等交易写入区块才能到账。自行刷新页面:)',
              showClose: true,
              type: 'success',
              duration: 30000
            })
          } else {
            this.$message({
              message: res.data.message || res.data.data,
              showClose: true,
              type: 'warning'
            })
          }
        })
      } else {
        this.$message({ message: '节点暂不可用，请等待 / 点击刷新', type: 'warning' })
      }
    }
  }
  // created () {
  //   this.account = getAccount()
  //   if (this.account) {
  //     getBalance(this.account).then(res => {
  //       if (res.status === 200) {
  //         this.balance = Math.round(res.data / 1000000000000000)
  //       }
  //     })
  //   }
  // }
}
</script>
