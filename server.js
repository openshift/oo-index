var config      = require('config'),
    restify     = require('restify'),
    fs          = require('fs')

var app         = restify.createServer()

app.use(restify.queryParser())
app.use(restify.CORS())
app.use(restify.fullResponse())

// Routes
app.get(/\/quickstart.json/, function myHandler(req, res, next) {
  var data = fs.readFileSync(__dirname + '/quickstart.json')
  var json = JSON.parse(data.toString())
  res.json(200, json)
});
app.get(/\/.*/, restify.serveStatic({'directory': './static/', 'default':"index.html"}));

app.listen(config.port, config.ip, function () {
  console.log( "Listening on " + config.ip + ", port " + config.port )
});
