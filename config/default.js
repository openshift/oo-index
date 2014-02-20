module.exports = {
  port: process.env.PORT || process.env.OPENSHIFT_NODEJS_PORT || 3000,
  ip: process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1',

  session_secret: 'open sesame',

  oauth_key: process.env.OAUTH_KEY,
  oauth_secret: process.env.OAUTH_SECRET,
  oauth_callback: '//' + process.env.OPENSHIFT_APP_DNS + '/auth/callback'
}
