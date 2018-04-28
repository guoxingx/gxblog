<template>
  <el-row>
    <el-col :xs="24" :sm="6" :md="6" :lg="5" :xl="4">
      <div class="left">
        <h1>BetOnEther</h1>
        <h2>基于以太坊测试链</h2>
        <account></account>
        <div class="list">
          <boe-list-cell v-for="boe in boe_list" :key="boe" :boe="boe"></boe-list-cell>
        </div>
      </div>
    </el-col>
    <el-col :xs="24" :sm="18" :md="16" :lg="14" :xl="12" class="board">
      <h2>{{ boe.league }} round {{ boe.round }}</h2>
      <el-row>
        <el-col :span="11">
          <div class="team">
            <img :src="boe.home_image"><h4>{{ boe.home }}</h4>
          </div>
        </el-col>
        <el-col :span="2" class="vs"><h3>vs</h3></el-col>
        <el-col :span="11">
          <div class="team" :xs="12">
            <img :src="boe.visiting_image"><h4>{{ boe.visiting }}</h4>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="12">
        <el-col :span="6" :offset="3">
          <h5>主胜</h5>
          <el-card shadow="hover">
            <el-button type="text" @click="bet(0)">
              {{ boe.win_odds / 1000 }}
            </el-button>
          </el-card>
        </el-col>
        <el-col :span="6" :offset="0">
          <h5>平局</h5>
          <el-card shadow="hover">
            <el-button type="text" @click="bet(1)">
              {{ boe.draw_odds / 1000 }}
            </el-button>
          </el-card>
        </el-col>
        <el-col :span="6" :offset="0">
          <h5>客胜</h5>
          <el-card shadow="hover">
            <el-button type="text" @click="bet(2)">
              {{ boe.lose_odds / 1000 }}
            </el-button>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="12">
        <h3>已下注</h3>
      </el-row>

      <el-row :gutter="12">
        <div v-if="1">
          <h3>兑奖！</h3>
        </div>
      </el-row>

    </el-col>
  </el-row>
</template>

<script>
import { getBetOnEtherList } from '../requests'

export default {
  name: 'blog_list',
  components: {
    'boe-list-cell': () => import('./boe_list_cell.vue'),
    'account': () => import('./account')
  },
  data () {
    return {
      boes_count: 0,
      boe_list: [],
      boe: {}
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
    })
  },
  methods: {
    bet (beton) {
      alert(beton)
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
  margin-top: 100px;
  text-align: center;
}
.board {
  text-align: center;
}
</style>
