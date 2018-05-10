
export let gitmentConfig = {
  owner: 'guoxingx',
  repo: 'blog-comments',
  oauth: {
    client_id: '9777264851181483235d',
    client_secret: '339ccabbe2c9c69cd9dc133e813d34bb8b2ba2e9'
  }
}

if (process.env.NODE_ENV === 'development') {
  gitmentConfig = {
    owner: 'guoxingx',
    repo: 'blog-comments-test',
    oauth: {
      client_id: '15f2b76b369424268fd6',
      client_secret: 'a0c16b867fd960b011c074709590a43a87807138'
    }
  }
}
