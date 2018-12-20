const path = require('path')

module.exports = {
  extensions: ['.js', '.mjs', '.json', '.jsx', '.css', '.scss'],
  modules: [
    path.resolve(__dirname, '../src'),
    path.resolve(__dirname, '../node_modules'),
  ],
}
