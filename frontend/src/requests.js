
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

var HOST = 'http://localhost'

if (process.env.NODE_ENV === 'development') {
  HOST = 'http://localhost:5000'
}

export function getArticleList () {
  return get(HOST + '/api/articles')
}

export function getArticle (id) {
  return get(HOST + '/api/articles/' + id)
}

export function getHtml (url) {
  return get(HOST + url)
}

export function getBetOnEtherList () {
  return get(HOST + '/api/betonethers')
}

export function getBetOnEther (id) {
  return get(HOST + '/api/betonethers/' + id)
}

export function getBalance(address) {
  return get(HOST + '/api/accounts/' + address)
}
