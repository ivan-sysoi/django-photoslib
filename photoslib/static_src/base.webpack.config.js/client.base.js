const path = require('path')

const isDev = process.env.NODE_ENV === 'development'

module.exports = {
  target: 'web',
  output: {
    path: path.resolve(__dirname, '..', (isDev ? 'dev_dist' : 'dist'), 'site'),
    filename: '[name].js',
  },
  module: {
    rules: [
      {
        oneOf: require('./loaders').defaultLoaders,
      },
    ],
  },
  resolve: require('./resolvers'),
  plugins: require('./plugins'),
  node: {
    dgram: 'empty',
    fs: 'empty',
    net: 'empty',
    tls: 'empty',
    child_process: 'empty',
  },
  optimization: {
    namedModules: true,
    noEmitOnErrors: true,
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'all',
        },
      },
    },
  },
  stats: {
    cached: false,
    cachedAssets: false,
    chunks: false,
    chunkModules: false,
    colors: true,
    hash: false,
    modules: false,
    reasons: false,
    timings: true,
    version: false,
  },
}
