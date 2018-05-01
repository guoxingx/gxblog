<template>
  <el-row>
    <el-col :xs="24" :sm="6" :md="6" :lg="5" :xl="4">
      <div class="left">
        <h1>BetOnEther</h1>
        <h2>基于以太坊测试链</h2>
        <account :balance="balance" :account="account"></account>
        <div class="list">
          <boe-list-cell v-for="boe in boe_list" :key="boe" :boe="boe"></boe-list-cell>
        </div>
      </div>
    </el-col>

    <el-col :xs="24" :sm="18" :md="16" :lg="14" :xl="12" class="board">
      <h2>{{ boe.league }} round {{ boe.round }}</h2>
      <h4 :style="boe.ended ? 'color: #E6A23C;':'color: #409EFF;'">
        {{ boe.ended ? '已结束' : '进行中' }}
      </h4>
      <el-button type="primary" @click="refresh" round>点我刷新</el-button>
      <el-row>
        <el-col :span="11">
          <div class="team">
            <img :src="boe.home_image"><h4>{{ boe.home }}</h4>
          </div>
        </el-col>
        <el-col :span="2" class="vs">
          <h3>vs</h3>
        </el-col>
        <el-col :span="11">
          <div class="team" :xs="12">
            <img :src="boe.visiting_image"><h4>{{ boe.visiting }}</h4>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="12">
        <el-col :span="6" :offset="3">
          <h5>主胜</h5>
          <el-card shadow="hover" :class="boe.result===0? 'result':''">
            <el-button type="text" v-popover:beton0>
              {{ boe.win_odds / 1000 }}
            </el-button>
          </el-card>
        </el-col>
        <el-col :span="6" :offset="0">
          <h5>平局</h5>
          <el-card shadow="hover" :class="boe.result===1? 'result':''">
            <el-button type="text" v-popover:beton1>
              {{ boe.draw_odds / 1000 }}
            </el-button>
          </el-card>
        </el-col>
        <el-col :span="6" :offset="0">
          <h5>客胜</h5>
          <el-card shadow="hover" :class="boe.result===2? 'result':''">
            <el-button type="text" v-popover:beton2>
              {{ boe.lose_odds / 1000 }}
            </el-button>
          </el-card>
        </el-col>
      </el-row>

      <el-popover ref="beton0" placement="top" width="260" v-model="visible0">
        <el-row>
          <el-col :span="20">
            <el-input type="number" v-model="amount" placeholder="输入金额(finney)"></el-input>
            <el-input type="password" v-model="password" placeholder="输入密码"></el-input>
          </el-col>
          <el-col :span="3" :offset="1">
            <el-button type="Blue" icon="el-icon-check" @click="bet(0)" circle></el-button>
          </el-col>
        </el-row>
      </el-popover>

      <el-popover ref="beton1" placement="top" width="260" v-model="visible1">
        <el-row>
          <el-col :span="20">
            <el-input type="number" v-model="amount" placeholder="输入金额(finney)"></el-input>
            <el-input type="password" v-model="password" placeholder="输入密码"></el-input>
          </el-col>
          <el-col :span="3" :offset="1">
            <el-button type="Blue" icon="el-icon-check" @click="bet(1)" circle></el-button>
          </el-col>
        </el-row>
      </el-popover>

      <el-popover ref="beton2" placement="top" width="260" v-model="visible2">
        <el-row>
          <el-col :span="20">
            <el-input type="number" v-model="amount" placeholder="输入金额(finney)"></el-input>
            <el-input type="password" v-model="password" placeholder="输入密码"></el-input>
          </el-col>
          <el-col :span="3" :offset="1">
            <el-button type="Blue" icon="el-icon-check" @click="bet(2)" circle></el-button>
          </el-col>
        </el-row>
      </el-popover>

      <el-col :span="18" :offset="3">
        <keep-alive>
          <boe-bets style="margin-top: 20px;" :boe="this.boe" :betList="this.betList" :account="this.account"></boe-bets>
        </keep-alive>
      </el-col>

      <el-col :span="18" :offset="3">
        <p>注：只有在交易被区块写入之后，下注 / 提现 / 余额更新 等接口才算正式完成</p>
        <p>因为作者很懒 ...请好好利用"刷新"按钮。<strong>暂时的</strong></p>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
import { getBetOnEtherList, betOnEtherBet, getBetOnEtherBetList, getBalance } from '../requests'
import { getAccount } from '../account'

export default {
  name: 'blog_list',
  components: {
    'boe-list-cell': () => import('./boe_list_cell.vue'),
    'account': () => import('./account'),
    'boe-bets': () => import('./boe_bets')
  },
  // watch: {
  //   '$route' (to, from) {
  //     alert(to, from)
  //   }
  // },
  beforeRouteUpdate (to, from, next) {
    if (to.params.id !== this.boe.id) {
      for (var i in this.boe_list) {
        if (this.boe_list[i].id === to.params.id) {
          this.boe = this.boe_list[i]
          this.getBetList()
        }
      }
    }
    next()
  },
  data () {
    return {
      boes_count: 0,
      boe_list: [],
      boe: {},
      betList: [],
      visible0: false,
      visible1: false,
      visible2: false,
      balance: 0,
      account: getAccount()
    }
  },
  created () {
    var bid = this.$route.params.id
    getBetOnEtherList().then(res => {
      for (var i in res.data) {
        if (res.data[i].id === Number(bid)) { this.boe = res.data[i] }
      }
      this.boes_count = res.data.length
      this.boe_list = res.data
      this.getBetList()
    })

    this.account = getAccount()
    if (this.account) {
      getBalance(this.account).then(res => {
        if (res.status === 200) {
          this.balance = Math.round(res.data / 1000000000000000)
        }
      })
    }
  },
  methods: {
    bet (beton) {
      var address = getAccount()
      if (!this.boe.id) { this.$message({ message: 'id未找到', type: 'warning' }) }
      if (!this.amount) { this.$message({ message: '金额未填写', type: 'warning' }) }
      if (!address) { this.$message({ message: '账号未找到', type: 'warning' }) }
      if (!this.password) { this.$message({ message: '密码未填写', type: 'warning' }) }

      if (!this.boe.ended && this.boe.id && beton != null && this.amount && address && this.password) {
        betOnEtherBet(this.boe.id, beton, this.amount, address, this.password).then(res => {
          if (res.status === 200) {
            if (res.data.code === 0) {
              this.$message({ message: '下注成功！请等待数据写入区块...', type: 'success' })
            } else {
              this.$message({ message: '下注过大，庄家保证金不足！', type: 'warning' })
            }
          } else {
            this.$message({ message: '下注失败:(', type: 'warning' })
          }
          if (beton === 0) { this.visible0 = false }
          if (beton === 1) { this.visible1 = false }
          if (beton === 2) { this.visible2 = false }
        })
      }
    },

    getBetList () {
      var account = getAccount()
      if (account) {
        getBetOnEtherBetList(this.boe.id, getAccount()).then(res => {
          if (res.status === 200) {
            var betList = []
            for (var i in res.data) {
              var data = res.data[i]
              betList.push({
                beton: data[0],
                amount: Math.round(data[1] / 1000000000000000),
                odds: data[2] / 1000,
                profit: Math.round(data[3] / 1000000000000000),
                withdrawed: data[4]
              })
            }
            this.betList = betList
          }
        })
      }
    },

    refresh () {
      var bid = this.boe.id
      getBetOnEtherList().then(res => {
        for (var i in res.data) {
          if (res.data[i].id === Number(bid)) { this.boe = res.data[i] }
        }
        this.boes_count = res.data.length
        this.boe_list = res.data
        this.getBetList()

        this.$message({ message: '刷新成功', type: 'success' })
      })

      this.account = getAccount()
      if (this.account) {
        getBalance(this.account).then(res => {
          if (res.status === 200) {
            this.balance = Math.round(res.data / 1000000000000000)
          }
        })
      }
    }

  }
}
</script>

<style>
.left {
  text-align: center;
}
.list {
  margin: 10px;
}
.team {
  margin: 0 auto;
  text-align: center;
}
.team img {
  height: 200px;
}
.vs {
  margin-top: 200px;
  text-align: center;
}
.board {
  text-align: center;
}
.result {
  background: #67C23A;
}
.result span {
  color: white;
}
</style>
