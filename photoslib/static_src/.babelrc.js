const isDev = process.env.NODE_ENV === 'development'

const env = {
  isDev,
}

module.exports = {
  "compact": true,
  "presets": [
    [
      "@babel/preset-env",
      {
        "modules": false,
        "targets": {
          "browsers": [
            "last 2 versions",
            "ie >= 9"
          ]
        }
      }
    ],
    "@babel/preset-react",
  ],
  "plugins": [
    ["transform-define", env],
    "@babel/plugin-proposal-object-rest-spread",
    "@babel/plugin-proposal-class-properties",
    "@babel/plugin-proposal-export-default-from",
    "@babel/plugin-syntax-dynamic-import"
  ],
  "env": {
    "test": {
      "plugins": [
        "@babel/plugin-transform-modules-commonjs"
      ]
    },
    "production": {
      "plugins": [
        "transform-react-remove-prop-types"
      ]
    }
  }
}
