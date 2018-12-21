const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin")
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
      }),
      new OptimizeCSSAssetsPlugin({}),
    ],
  },
}

module.exports = config
