<template>
  <div style="text-align: left">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>已下注</span>
        <el-button style="float: right; padding: 3px 0; font-size: 18px;" type="text" v-popover:withdrawBoard>提现！</el-button>
      </div>

      <el-popover ref="withdrawBoard" placement="top" width="260" v-model="visible0">
        <el-row>
          <el-col :span="20">
            <el-input type="password" v-model="password" placeholder="输入密码"></el-input>
            <p type='warning'>无意义的提现会浪费gas(手续费)</p>
          </el-col>
          <el-col :span="3" :offset="1">
            <el-button type="Blue" icon="el-icon-check" @click="withdraw()" circle></el-button>
          </el-col>
        </el-row>
      </el-popover>

      <el-table :data="betList" style="width: 100%">

        <el-table-column label="赛果">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.beton===0" :type="boe.result===0 ? 'success' : 'info'">主胜</el-tag>
            <el-tag v-if="scope.row.beton===1" :type="boe.result===1 ? 'success' : 'info'">平局</el-tag>
            <el-tag v-if="scope.row.beton===2" :type="boe.result===2 ? 'success' : 'info'">客胜</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额(finney)"></el-table-column>
        <el-table-column prop="odds" label="赔率"></el-table-column>
        <el-table-column prop="profit" label="收益(finney)"></el-table-column>
        <el-table-column prop="withdrawed" label="提现">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.withdrawed" :type="success">已提现</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { betOnEtherWithdraw } from '@/js/requests'

export default {
  props: ['boe', 'betList', 'account', 'nodeStatus'],
  data () {
    return {
      visible0: false
    }
  },
  methods: {
    withdraw () {
      if (this.nodeStatus === 0) {
        var bid = this.boe.id
        if (this.boe.ended) {
          betOnEtherWithdraw(bid, this.account, this.password).then(res => {
            if (res.data.code === 30001) {
              this.$message({ message: '操作过于频繁，15秒后重试', type: 'warning' })
            } else {
              this.$message({ message: '提现成功！请等待数据写入区块...', type: 'success' })
              this.visible0 = false
            }
          })
        } else {
          this.$message({ message: '请等待比赛结束 / 或刷新数据', type: 'warning' })
        }
      } else {
        this.$message({ message: '节点暂不可用，请等待 / 点击刷新', type: 'warning' })
      }
    }
  }
}
</script>
