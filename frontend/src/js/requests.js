
import axios from 'axios'

export function get (url) {
  return new Promise(function (resolve, reject) {
    axios.get(url).then(res => {
      resolve(res)
    })
  })
}

export function post (url, data) {
  return new Promise(function (resolve, reject) {
    axios.post(url, data).then(res => {
      resolve(res)
    })
  })
}

// var HOST = 'http://116.62.200.91'
var HOST = ''

if (process.env.NODE_ENV === 'development') {
  HOST = 'http://localhost:5000'
}

export function getBlogList () {
  return get(HOST + '/api/blogs')
}

export function getBlog (id) {
  return get(HOST + '/api/blogs/' + id)
}

export function getHtml (url) {
  return get(HOST + url)
}

export function getBetOnEtherList (index = 0) {
  return get(HOST + '/api/eth/betonethers?index=' + index)
}

export function getBetOnEther (id) {
  return get(HOST + '/api/eth/betonethers/' + id)
}

export function registerAccount (password) {
  return post(HOST + '/api/eth/accounts', {password: password})
}

export function getBalance (address) {
  return get(HOST + '/api/eth/accounts/' + address + '/balance')
}

export function betOnEtherBet (id, beton, amount, address, password) {
  return post(
    HOST + '/api/eth/betonethers/' + id + '/bets',
    {
      beton: beton,
      amount: amount,
      address: address,
      password: password
    })
}

export function getBetOnEtherBetList (id, address) {
  return get(HOST + '/api/eth/betonethers/' + id + '/bets?address=' + address)
}

export function betOnEtherWithdraw (id, address, password) {
  return post(
    HOST + '/api/eth/betonethers/' + id + '/withdraw',
    {
      address: address,
      password: password
    })
}

export function requestTestEther (address) {
  if (process.env.NODE_ENV === 'development') {
    return post(
      HOST + '/api/eth/testether',
      {
        address: address
      }
    )
  } else {
    return get('http://faucet.ropsten.be:3001/donate/' + address)
  }
}

export function getNodeStatus () {
  return get(HOST + '/api/eth/status')
}
