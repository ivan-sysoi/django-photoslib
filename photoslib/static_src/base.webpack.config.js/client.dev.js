const baseConfig = require('./client.base')

const config = {
  ...baseConfig,
  mode: 'development',
  devtool: 'eval-source-map',
  performance: {
    hints: false,
  },
}

module.exports = config
