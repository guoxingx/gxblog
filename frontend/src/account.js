
var AccountCookieName = 'testguoxingethaccount'

if (process.env.NODE_ENV === 'development') {
  AccountCookieName = 'devguoxingethaccount'
} else if (process.env.NODE_ENV === 'product') {
  AccountCookieName = 'proguoxingethaccount'
}

export function setCookie (name, value) {
  var date = new Date()
  date.setTime(date.getTime() + (60 * 60 * 24 * 253))
  var expires = 'expires=' + date.toGMTString()
  document.cookie = name + '=' + value + '; ' + expires
}

export function delCookie (name) {
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT'
}

export function getCookie (name) {
  var ca = document.cookie.split(';')
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i].trim()
    if (c.indexOf(name) === 0) {
      var value = c.split('=')[1]
      if (value && value.length > 0) {
        setCookie(name, value)
      }
      return value
    }
  }
  return null
}

export function getAccount () {
  return getCookie(AccountCookieName)
}

export function setAccount (address) {
  setCookie(AccountCookieName, address)
}

export function logoutAccount () {
  delCookie(AccountCookieName)
}
