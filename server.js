var fs             = require('fs'),
    config         = require('config'),
    restify        = require('restify'),
    connect        = require('connect'),
    passport       = require('passport'),
    GitHubStrategy = require('passport-github').Strategy;

var app = restify.createServer();

// Restify-Connect compatibility

app.use(function(req, res, next){
    req.originalUrl = req.url;
    next();
});

// Enable Connect-based sessions

app.use(connect.cookieParser());
app.use(connect.session({ secret : config.session_secret, key: 'sid' }));

// Initialize Passport for authentication

app.use(passport.initialize());
passport.use(
    new GitHubStrategy({
        clientID: config.oauth_key,
        clientSecret: config.oauth_secret,
        callbackURL: config.oauth_callback,
        scope: 'repo,user,gist'
    },
    function(accessToken, refreshToken, profile, done) {
        profile.accessToken = accessToken;
        return done(null, profile);
    }
));

// Restify configuration

app.use(restify.queryParser())
app.use(restify.CORS())
app.use(restify.fullResponse())

// Authentication related handlers

app.get('/auth', passport.authorize('github'));

app.get('/auth/callback', passport.authorize('github'), function(req, res) {
    req.session.user = req.account.username;
    req.session.accessToken = req.account.accessToken;
    res.writeHead(302, { 'Location': '/' });
    res.end();
});

app.get('/auth/user', function(req, res) {
    res.json(200, { username: req.session.user, accessToken: req.session.accessToken  });
});

// OO-index related handlers

app.get(/\/quickstart.json/, function myHandler(req, res, next) {
  var data = fs.readFileSync(__dirname + '/quickstart.json')
  var json = JSON.parse(data.toString())
  res.json(200, json)
});

app.get(/\/.*/, restify.serveStatic({'directory': './static/', 'default':"index.html"}));

app.listen(config.port, config.ip, function () {
  console.log( "Listening on " + config.ip + ", port " + config.port )
});
