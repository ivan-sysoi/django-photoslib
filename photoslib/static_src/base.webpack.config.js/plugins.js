const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const webpack = require('webpack')

module.exports = [
  new MiniCssExtractPlugin({
    filename: '[name].css',
  }),
  new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
]
