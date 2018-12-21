const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const defaultFileLoader = {
  loader: 'file-loader',
  options: {
    name: 'assets/[name].[hash:8].[ext]',
  },
}

const defaultBabelLoader = {
  loader: 'babel-loader',
  options: {
    babelrc: true,
    extends: path.resolve(__dirname, '../.babelrc.js'),
  }
}

const responsiveLoader = {
  loader: 'responsive-loader',
  exclude: /./,
}

const babelLoader = {
  test: /\.(js|jsx)$/,
  exclude: /node_modules/,
  ...defaultBabelLoader,
}

const svgReactLoader = {
  test: /\.svg$/,
  exclude: /node_modules/,
  use: [
    defaultBabelLoader,
    {
      loader: 'svg-react-loader',
      query: {
        classIdPrefix: '[name]-[hash:8]__',
      },
    }
  ],
}

const svgTransformLoader = {
  test: /\.svg(\?.*)?$/,
  exclude: /node_modules/,
  use: [
    defaultFileLoader,
    {
      loader: 'svg-transform-loader',
    },
  ],
}

const imageLoader = {
  test: /\.(gif|png|jpe?g)$/i,
  use: [
    defaultFileLoader,
    {
      loader: 'image-webpack-loader',
      options: {
        bypassOnDebug: true, // webpack@1.x
        disable: true, // webpack@2.x and newer
        mozjpeg: {
          progressive: true,
          quality: 75,
        },
        // optipng.enabled: false will disable optipng
        optipng: {
          enabled: false,
        },
        pngquant: {
          quality: '65-90',
          speed: 4,
        },
        gifsicle: {
          interlaced: false,
        },
        // the webp option will enable WEBP
        webp: {
          quality: 75,
        },
      },
    },
  ],
}

const urlLoader = {
  test: /\.(eot|woff2?)$/,
  loader: require.resolve('url-loader'),
  options: {
    limit: 2048,
    name: 'assets/[name].[hash:8].[ext]',
  },
}

const fileLoader = {
  exclude: [/\.(js|css|mjs|html|json)$/],
  use: [
    defaultFileLoader,
  ],
}

const cssLoader = {
  test: /\.css$/,
  use: [
    MiniCssExtractPlugin.loader,
    {
      loader: 'css-loader',
      options: {
        sourceMap: true,
        importLoaders: 1,
      },
    },
    {
      loader: 'postcss-loader',
      options: {
        sourceMap: true,
        config: {
          path: path.resolve(__dirname, '../'),
        },
      },
    },
    {
      loader: 'resolve-url-loader',
    },
  ],
}

const getSassLoader = ({ modules = true, test = /\.scss$/ } = {}) => {
  return {
    test,
    exclude: /node_modules/,
    use: [
      MiniCssExtractPlugin.loader,
      {
        loader: 'css-loader',
        options: {
          ...(modules ? {
            modules: true,
            importLoaders: 3,
            localIdentName: '[local]--[hash:base64:5]',
          } : {}),
        },
      },
      {
        loader: 'postcss-loader',
        options: {
          config: {
            path: path.resolve(__dirname, '../'),
          },
        },
      },
      {
        loader: 'resolve-url-loader',
        options: {
          keepQuery: true // <- this!
        },
      },
      {
        loader: 'sass-loader',
        options: {
          sourceMap: true,
        },
      },
    ],
  }
}

module.exports = {
  getSassLoader,
  svgReactLoader,
  svgTransformLoader,
  babelLoader,
  defaultBabelLoader,
  cssLoader,
  urlLoader,
  fileLoader,
  imageLoader,
  responsiveLoader,

  defaultLoaders: [
    svgTransformLoader,
    imageLoader,
    babelLoader,
    getSassLoader(),
    cssLoader,
    urlLoader,
    fileLoader,
  ],
}
