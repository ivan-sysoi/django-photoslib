const path = require('path')

const isDev = process.env.NODE_ENV === 'development'
const rootConfig = require('./base.webpack.config.js')
const baseLoaders = require('./base.webpack.config.js/loaders')

module.exports = {
  ...rootConfig,
  name: 'photo_lib',
  module: {
    rules: [
      {
        oneOf: [
          baseLoaders.svgReactLoader,
          baseLoaders.imageLoader,
          baseLoaders.babelLoader,
          baseLoaders.getSassLoader(),
          baseLoaders.cssLoader,
          baseLoaders.urlLoader,
          baseLoaders.fileLoader,
        ],
      },
    ],
  },
  entry: {
    'photo-field': ['@babel/polyfill/noConflict', path.resolve(__dirname, 'src/index.js')],
  },
  externals: {
    react: 'React',
    'react-dom': 'ReactDOM',
  },
  output: {
    ...rootConfig.output,
    path: path.resolve(__dirname, `../static/${isDev ? 'dev-' : ''}photoslib`),
  },
}
