const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin")
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin');

const baseConfig = require('./client.base')

const config = {
  ...baseConfig,
  mode: 'production',
  devtool: 'source-map',
  optimization: {
    ...baseConfig.optimization,
    minimizer: [
      new TerserPlugin({
        cache: true,
        parallel: true,
        //terserOptions: {
        //      mangle: true,
        //      ie8: false,
        //}
      }),
      //new UglifyJsPlugin({
      //  cache: true,
      //  parallel: true,
      //  uglifyOptions: {
      //    mangle: true,
      //    ie8: false,
      //  },
      //}),
      new OptimizeCSSAssetsPlugin({}),
    ],
  },
}

module.exports = config
