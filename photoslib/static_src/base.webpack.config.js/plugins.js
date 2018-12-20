const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const webpack = require('webpack')

module.exports = [
  new MiniCssExtractPlugin({
    filename: '[name].css',
      //process.env.NODE_ENV === 'development' ? '[name].css' : '[name].[contenthash].css',
    //chunkFilename:
    //  process.env.NODE_ENV === 'development' ? '[id].css' : '[id].[contenthash].css',
  }),
  new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
]
