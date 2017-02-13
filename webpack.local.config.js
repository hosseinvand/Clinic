var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

var config = require('./webpack.config.js')

var ip = 'localhost'

config.devtool = "#eval-source-map"

// Use webpack dev server
config.entry = {
  App: [
    'webpack-dev-server/client?http://' + ip + ':3000',
    'webpack/hot/only-dev-server',
    'babel-polyfill',
    './reactjs/index',
  ],
}

// override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://' + ip + ':3000' + '/static/'

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoErrorsPlugin(),
  new BundleTracker({filename: './webpack-stats-local.json'}),
])

// Add a loader for JSX files with react-hot enabled
// config.module.loaders.push(
//   { test: /\.jsx?$/, exclude: /node_modules/, loaders: ['react-hot', 'babel'] }
// )

module.exports = config
