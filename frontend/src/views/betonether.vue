<template>
  <div>
  <el-row>
    <el-col :xs="24" :sm="24" :md="24" :lg="5" :xl="8" class="right" style="float: right">
      <div class="status">
        <el-button :type="nodeStatus===0 ? 'success' : 'danger'" @click="refreshNodeStatus(true)" round>
          当前状态: {{ nodeStatusString }}
        </el-button>
      </div>
      <div class="status">
        <el-button :type="nodeStatus===0 ? 'success' : 'danger'" @click="refreshNodeStatus(true)" round>
          连接节点数: {{ peerCount }}
        </el-button>
      </div>
    </el-col>

    <el-col :xs="24" :sm="6" :md="6" :lg="5" :xl="4">
      <div class="left">
        <h1>BetOnEther</h1>
        <h2>基于以太坊测试链</h2>
        <account :balance="balance" :account="account" :nodeStatus="nodeStatus"></account>
        <div class="list">
          <boe-list-cell
            v-for="boe in boeList" :key="boe" :boe="boe"
            v-on:click.native="chooseBoe(boe)">
          </boe-list-cell>
        </div>

        <div class="block">
          <el-pagination small layout="prev, pager, next" page-size="3"
          :total="boeTotalCount"
          :current-page="boeCurrentPage"
          @current-change="changePage"></el-pagination>
        </div>

      </div>
    </el-col>

    <el-col v-if="!boe.id" :xs="24" :sm="18" :md="16" :lg="14" :xl="12" class="board">
      <h2>未选择比赛</h2>
    </el-col>
    <el-col v-if="boe.id" :xs="24" :sm="18" :md="16" :lg="14" :xl="12" class="board">
      <h2>{{ boe.league }} round {{ boe.round }}</h2>
      <h4 :style="boe.ended ? 'color: #E6A23C;':'color: #409EFF;'">
        {{ boe.ended ? '已结束' : '进行中' }}
      </h4>
      <el-button type="primary" @click="refresh(true)" round>点我刷新</el-button>
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
          <el-card shadow="hover" v-bind:class="{ result: boe.result===0 }">
            <el-button type="text" v-popover:beton0>
              {{ boe.win_odds / 1000 || 0 }}
            </el-button>
          </el-card>
        </el-col>
        <el-col :span="6" :offset="0">
          <h5>平局</h5>
          <el-card shadow="hover" v-bind:class="{ result: boe.result===1 }">
            <el-button type="text" v-popover:beton1>
              {{ boe.draw_odds / 1000 || 0 }}
            </el-button>
          </el-card>
        </el-col>
        <el-col :span="6" :offset="0">
          <h5>客胜</h5>
          <el-card shadow="hover" v-bind:class="{ result: boe.result===2 }">
            <el-button type="text" v-popover:beton2>
              {{ boe.lose_odds / 1000 || 0 }}
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
          <boe-bets style="margin-top: 20px;" :boe="this.boe" :betList="this.betList" :account="this.account" :nodeStatus="nodeStatus"></boe-bets>
        </keep-alive>
      </el-col>

      <el-col :span="18" :offset="3">
        <p>注：只有在交易被区块写入之后，下注 / 提现 / 余额更新 等接口才算正式完成</p>
        <p>因为作者很懒 ...请好好利用"刷新"按钮。<strong>暂时的</strong></p>
      </el-col>
    </el-col>
  </el-row>
  </div>
</template>

<script>
import { getBetOnEtherList, betOnEtherBet, getBetOnEtherBetList, getBalance, getNodeStatus } from '@/js/requests'
import { getAccount } from '@/js/account'

export default {
  name: 'blog_list',
  components: {
    'boe-list-cell': () => import('../components/boe_list_cell.vue'),
    'account': () => import('../components/account'),
    'boe-bets': () => import('../components/boe_bets')
  },
  beforeRouteUpdate (to, from, next) {
    if (to.params.id !== this.boe.id) {
      for (var i in this.boeList) {
        if (this.boeList[i].id === to.params.id) {
          this.boe = this.boeList[i]
          this.getBetList()
        }
      }
    }
    next()
  },
  data () {
    return {
      boeList: [],
      boe: {},
      betList: [],
      visible0: false,
      visible1: false,
      visible2: false,
      balance: 0,
      account: getAccount(),
      nodeStatus: -1,
      nodeStatusString: 'unknown',
      peerCount: 0,
      boeCurrentPage: this.$route.params.page,
      boeTotalCount: 0
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    chooseBoe (boe) { this.boe = boe },

    bet (beton) {
      if (this.nodeStatus === 0) {
        if (this.betCheck()) {
          return
        }
        betOnEtherBet(this.boe.id, beton, this.amount, getAccount(), this.password).then(res => {
          if (res.status === 200) {
            this.betResponse(res.data.code)
          } else {
            this.$message({ message: '下注失败:(', type: 'warning' })
          }
          if (beton === 0) { this.visible0 = false }
          if (beton === 1) { this.visible1 = false }
          if (beton === 2) { this.visible2 = false }
        })
      } else {
        this.$message({ message: '节点暂不可用，请等待 / 点击刷新', type: 'warning' })
      }
    },

    betCheck () {
      if (this.boe.ended) {
        this.$message({ message: '该轮游戏已结束', type: 'warning' })
        return 1
      }
      var address = getAccount()
      if (!this.boe.id) {
        this.$message({ message: 'id未找到', type: 'warning' })
        return 1
      }
      if (!this.amount) {
        this.$message({ message: '金额未填写', type: 'warning' })
        return 1
      }
      if (!address) {
        this.$message({ message: '账号未找到', type: 'warning' })
        return 1
      }
      if (!this.password) {
        this.$message({ message: '密码未填写', type: 'warning' })
        return 1
      }
      return 0
    },

    betResponse (code) {
      if (code === 0) {
        this.$message({ message: '下注成功！请等待数据写入区块...', type: 'success' })
      } else if (code === 30001) {
        this.$message({ message: '操作过于频繁，15秒后重试', type: 'warning' })
      } else if (code === 1) {
        this.$message({ message: '密码错误', type: 'warning' })
      } else {
        this.$message({ message: '下注过大，庄家保证金不足！', type: 'warning' })
      }
    },

    getBetList () {
      var account = getAccount()
      if (account) {
        getBetOnEtherBetList(this.boe.id, getAccount()).then(res => {
          if (res.status === 200) {
            var betList = []
            var data = res.data.data
            for (var i in data) {
              var bet = data[i]
              betList.push({
                beton: bet[0],
                amount: Math.round(bet[1] / 1000000000000000),
                odds: bet[2] / 1000,
                profit: Math.round(bet[3] / 1000000000000000),
                withdrawed: bet[4]
              })
            }
            this.betList = betList
          }
        })
      }
    },

    refreshNodeStatus (isRefresh = false) {
      getNodeStatus().then(res => {
        if (res.status === 200) {
          var data = res.data.data
          this.nodeStatus = data.status
          this.nodeStatusString = data.message
          this.peerCount = data.peer_count
          if (isRefresh) {
            this.$message({ message: '状态刷新成功', type: 'success' })
          }
        }
      })
    },

    refresh (isRefresh = false) {
      this.refreshNodeStatus()

      getBetOnEtherList((this.$route.params.page - 1) * 3).then(res => {
        if (res.status === 200 && res.data.code === 0) {
          this.boeTotalCount = res.data.data.total
          this.boeList = res.data.data.data
          if (!this.boe.id) { this.boe = this.boeList[0] }
          this.getBetList()
          if (isRefresh) { this.$message({ message: '刷新成功', type: 'success' }) }
        }
      })

      this.account = getAccount()
      if (this.account) {
        getBalance(this.account).then(res => {
          if (res.status === 200) {
            this.balance = Math.round(res.data.data / 1000000000000000)
          }
        })
      }
    },

    changePage (val) {
      this.$router.push({ name: 'betonether', params: { page: val } })
    }

  },

  watch: {
    '$route' (to, from) {
      this.boe = {}
      this.refresh()
    }
  },

  beforeRouteEnter (to, from, next) {
    window.document.title = 'GXBlog - BetOnEther'
    next(vm => {})
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
/*.result {
  background: #67C23A;
}*/
.result span {
  color: #67C23A;
}
.status {
  text-align: center;
  padding: 5px 0;
}
</style>
