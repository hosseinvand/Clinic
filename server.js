const webpack = require('webpack')
const WebpackDevServer = require('webpack-dev-server')
const config = require('./webpack.local.config')

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  inline: true,
  historyApiFallback: true,
}).listen(8800, 'localhost', function (err, result) {
  if (err) {
    console.log(err)
  }

  console.log('Listening at ' + 'localhost' + ':8800')
})
