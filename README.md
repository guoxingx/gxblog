
# gxblog

[blog](http://no-money-for-service-for-now.com)

## go-ethereum
搭建了以太坊私有链 / 测试链 来部署智能合约

## flask
后端 集成web3.py，封装智能合约并提供rest api接口，也做配合和管理后台

## vue
前端

## nginx
配置见nginx/nginx.conf

## docker
用compose启动backend / nginx / mysql / go-ethereum 4个container

## 待解决
- 为了方便将私有链data推到了代码库，后端管理功能完善之后移除
- web3.py部署合约的方式不够优雅
- ropsten + light模式的节点太少导致找不到节点同步，在同步完成之前应该禁用相关接口
