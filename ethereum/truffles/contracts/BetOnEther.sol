pragma solidity ^0.4.19;

contract BetOnEther {

    address public host;      // 庄家
    uint public earnestMoney; // 保证金
    uint public pool;
    uint public balance;
    uint[3] bonuss;

    // 比赛结果
    enum Result { Win, Draw, Lose }

    // 
    enum Odds { Win, Draw, Lose }

    // 比赛信息
    struct Game {
        bytes32 home;      // 主队
        bytes32 visiting;  // 客队
        bytes32 remarks;   // 备注 比如赛事信息
        uint[3] oddss;     // [w d l] 赔率
        Result result;     // 比赛结果
    }

    Game public game;

    // 下注
    struct Bet {
        Result result;   // 比赛结果
        uint stake;      // 金额
        uint odds;       // 赔率
        uint profit;     // 获利
        bool withdrawed; // 已经提款
    }

    mapping (address => Bet) gambings;

    uint public betEnd;
    uint public gameEnd;

    modifier onlyHost() {
        require(msg.sender == host);
        _;
    }

    modifier onlyBefore(uint time_) {
        require(now < time_);
        _;
    }
    modifier onlyAfter(uint time_) {
        require(now > time_);
        _;
    }

    /// 创建
    constructor (bytes32 home_, bytes32 visiting_, bytes32 remarks_, uint[3] oddss_) public payable {
        host = msg.sender;
        earnestMoney = msg.value;

        // 利润
        balance = earnestMoney;

        // 比赛信息
        game.home = home_;
        game.visiting = visiting_;
        game.remarks = remarks_;
        game.oddss = oddss_;
    }

    /// 下注
    function bet (uint result) public payable onlyBefore(betEnd) {
        uint profit = msg.value * game.oddss[result];

        // 对应总奖金不能超过保证金
        require (bonuss[result] + profit < earnestMoney);

        gambings[msg.sender] = Bet({
            result: Result(result),
            stake: msg.value,
            odds: game.oddss[result],
            profit: profit,
            withdrawed: false
        });

        // 总奖池 + value
        pool += msg.value;

        // 对应总奖金 + profit
        bonuss[result] += profit;
    }

    /// 修改倍率
    function alterOdds (uint win, uint draw, uint lose) public onlyHost onlyBefore(betEnd) {
        game.oddss = [win, draw, lose];
    }
    
    /// 输入比赛结果
    function confirm (uint result) public onlyHost onlyAfter(gameEnd) {
        game.result = Result(result);

        // 利润 + 总奖池
        balance += pool;

        // 利润 - 对应奖金
        balance -= bonuss[result];
    }
    
    /// 提款
    function withdraw () public onlyAfter(gameEnd) {
        // bet_ = gambings[msg.sender];
        if (gambings[msg.sender].result == game.result && !gambings[msg.sender].withdrawed) {
            gambings[msg.sender].withdrawed = true;
            msg.sender.transfer(gambings[msg.sender].profit);
        }
    }
    
    /// 庄家提款
    function clear () public onlyHost onlyAfter(gameEnd) {
        // 提取剩余利润
        uint balance_ = balance;
        if (balance_ > 0) {
            balance = 0;
            msg.sender.transfer(balance_);
        }
    }
}
