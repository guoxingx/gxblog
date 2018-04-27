pragma solidity ^0.4.19;

/// @title 委托投票
contract VoteForWorldCup {   

    // 投票发起人
    address public host;

    enum Result {
        Champion,
        Second,
        Third,
        Fourth,
        QuartyFinal,
        RoundSixteen,
        GroupStage,
        Unknown
    }

    struct Voter {
        bool voted;  // 若为真，代表该人已投票
        uint vote;   // 投票提案的索引
    }

    // 参赛队伍
    struct Team {
        bytes32 name;   // 简称（最长32个字节）
        uint voteCount; // 得票数
        Result result;  // 最终成绩
        bool out;       // 是否已经被淘汰
    }

    // 一个 `Team` 结构类型的动态数组
    Team[] public participants;

    // 每个地址对应participants index的投票情况 
    mapping (address => Voter) public voters;

    modifier onlyHost() {
        require(msg.sender == host);
        _;
    }

    modifier notOut(uint _teamIndex) { 
        require (!participants[_teamIndex].out); 
        _; 
    }
    
    modifier notVoted() { 
        require (!voters[msg.sender].voted);
        _; 
    }

    /// 为 `participantNames` 中的每个提案，创建一个新的（投票）表决
    constructor (bytes32[] participantNames) public {
        host = msg.sender;

        //对于提供的每个提案名称，
        //创建一个新的 Team 对象并把它添加到数组的末尾。
        for (uint i = 0; i < participantNames.length; i ++) {
            participants.push(Team({
                name: participantNames[i],
                voteCount: 0,
                result: Result.Unknown,
                out: false
            }));
        }
    }

    /// 投给 `participants[teamIndex].name`.
    function vote (uint teamIndex) public notVoted notOut(teamIndex) {
        voters[msg.sender].voted = true;
        voters[msg.sender].vote = teamIndex;

        // 如果 `teamIndex` 超过了数组的范围，则会自动抛出异常，并恢复所有的改动
        participants[teamIndex].voteCount += 1;
    }

    /// 写入成绩
    function setResult (uint teamIndex, Result result, bool out) public onlyHost {
        participants[teamIndex].result = result;
        participants[teamIndex].out = out;
    }
}
