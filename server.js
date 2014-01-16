var config      = require('config'),
    restify     = require('restify'),
    fs          = require('fs')

var app         = restify.createServer()

app.use(restify.queryParser())
app.use(restify.CORS())
app.use(restify.fullResponse())

// Routes
app.get('/status', function (req, res, next)
{
  res.send("{status: 'ok'}");
});

app.get('/', function (req, res, next)
{
  var data = fs.readFileSync(__dirname + '/index.html');
  res.status(200);
  res.header('Content-Type', 'text/html');
  res.end(data.toString().replace(/host:port/g, req.header('Host')));
});
app.get(/\/css\/?.*/, restify.serveStatic({directory: './css/'}));
app.get(/\/js\/?.*/, restify.serveStatic({directory: './js/'}));
app.get(/\/img\/?.*/, restify.serveStatic({directory: './img/'}));

app.get(/\/quickstart.json/, function myHandler(req, res, next) {
  var data = fs.readFileSync(__dirname + '/quickstart.json')
  var json = JSON.parse(data.toString())
  console.dir(json)
  res.json(200, json)
});

app.listen(config.port, config.ip, function () {
  console.log( "Listening on " + config.ip + ", port " + config.port )
});
