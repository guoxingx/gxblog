pragma solidity ^0.4.19;

contract BetOnEther {

    address public host;      // 庄家
    uint public earnestMoney; // 保证金
    uint public pool;         // 总奖金池
    uint public balance;      // 庄家收益
    uint[3] public bonuss;    // [w d l] 对应总奖金
    uint[3] public oddss;     // [w d l] 赔率
    bool public ended;        // 游戏已结束
    bytes32 outerId;   // 链外ID

    // 比赛结果
    enum Result { Win, Draw, Lose }

    // 比赛信息
    struct Game {
        bytes32 home;      // 主队
        bytes32 visiting;  // 客队
        bytes32 remarks;   // 备注 比如开赛时间，赛事系列
        uint result;       // 比赛结果
    }

    Game public game;

    // 下注
    struct Bet {
        uint result;     // 比赛结果
        uint stake;      // 金额
        uint odds;       // 赔率
        uint profit;     // 获利
        bool withdrawed; // 已经提款
    }

    mapping (address => Bet[]) public bets;  // 所有玩家的下注信息
    uint public betCount;                    // 下注总数量
    address[] public players;                // 所有玩家 <如果有多次下注 会记录重复地址>

    uint public betEnd;
    uint public gameEnd;

    modifier onlyHost() {
        require(msg.sender == host);
        _;
    }

    modifier onlyBefore(uint _time) {
        require(now < _time);
        _;
    }

    modifier onlyAfter(uint _time) {
        require(now > _time);
        _;
    }

    modifier notEnd() { 
        require (!ended); 
        _; 
    }

    /// 创建
    constructor (bytes32 _home, bytes32 _visiting,
                 bytes32 _remarks, uint[3] _oddss,
                 uint _betTime, uint _gameTime,
                 bytes32 _outerId) public payable {
        host = msg.sender;
        oddss = _oddss;
        outerId = _outerId;

        betEnd = now + _betTime;
        gameEnd = betEnd + _gameTime;

        // 利润
        earnestMoney = msg.value;
        balance = earnestMoney;

        // 比赛信息
        game.home = _home;
        game.visiting = _visiting;
        game.remarks = _remarks;
    }

    /// Input earnestMoney
    function inputEarnestMoney () public onlyHost payable {
        earnestMoney += msg.value;
        balance = earnestMoney;
    }

    /// 下注
    function bet (uint _result) public payable onlyBefore(betEnd) {
        uint _profit = (msg.value * oddss[_result]) / 1000;

        // 对应总奖金不能超过保证金
        require ((bonuss[_result] + _profit) < earnestMoney);

        bets[msg.sender].push(Bet({
            result: _result,
            stake: msg.value,
            odds: oddss[_result],
            profit: _profit,
            withdrawed: false
        }));

        // 总奖池 + value
        pool += msg.value;

        // 对应总奖金 + _profit
        bonuss[_result] += _profit;

        betCount += 1;
        players.push(msg.sender);
    }

    /// 修改倍率
    function alterOdds (uint win, uint draw, uint lose) public onlyHost onlyBefore(betEnd) {
        oddss = [win, draw, lose];
    }

    /// 输入比赛结果
    // function confirm (uint _result) public onlyHost onlyAfter(gameEnd) {
    function confirm (uint _result) public onlyHost notEnd {        
        game.result = _result;
        ended = true;

        // 利润 + 总奖池
        balance += pool;

        // 利润 - 对应奖金
        balance -= bonuss[_result];
    }

    /// 提款
    // function withdraw () public onlyAfter(gameEnd) {
    function withdraw () public {
        require (ended);

        uint length = bets[msg.sender].length;
        uint amount = 0;
        
        for (uint i = 0; i < length; i ++) {
            var _bet = bets[msg.sender][i];
            if ((_bet.result == game.result) && !_bet.withdrawed) {
                amount += _bet.profit;
                _bet.withdrawed = true;
            }
        }

        if (amount > 0) {
            uint _amount = amount;
            amount = 0;
            msg.sender.transfer(_amount);
        }
    }

    /// 庄家提款
    // function clear () public onlyHost onlyAfter(gameEnd) {
    function clear () public onlyHost {
        require (ended);
        
        // 提取剩余利润
        uint _balance = balance;
        if (_balance > 0) {
            balance = 0;
            msg.sender.transfer(_balance);
        }
    }
}
