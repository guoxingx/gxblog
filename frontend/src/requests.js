
import axios from 'axios'

export function get (url) {
  return new Promise(function (resolve, reject) {
    axios.get(url).then(res => {
      resolve(res)
    })
  })
}

export function getArticleList () {
  return get('http://localhost/api/articles')
}

export function getArticle (id) {
  return get('http://localhost/api/articles/' + id)
}

export function getHtml (url) {
  return get('http://localhost' + url)
}
