const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');
const webpack = require('webpack');

module.exports = {
  entry: './js/app.jsx',
  output: {
    path: path.resolve(__dirname, '../../dist/www'),
    filename: 'uwsolar.js'
  },
  devtool: 'cheap-module-source-map',
  module: {
    rules: [
      {
        test: /\.html$/,
        exclude: /node_modules/,
        use: 'html-loader'
      },
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-es2015', '@babel/preset-react']
            }
          },
          {
            loader: 'eslint-loader',
            options: {
              "useEslintrc": false,
              "plugins": ["react"],
              "parserOptions": {
                "ecmaVersion": 6,
                "sourceType": "module",
                "ecmaFeatures": {
                  "jsx": true
                }
              },
              "env": {
                "es6": true,
                "browser": true,
                "node": true
              },
              "extends": ["eslint:recommended", "plugin:react/recommended"],
              "rules": {
                "array-bracket-spacing": [
                  1,
                  "always",
                  {
                    "singleValue": false,
                    "objectsInArrays": false,
                    "arraysInArrays": false
                  }
                ],
                "curly": [1, "all"],
                "default-case": 1,
                "guard-for-in": 1,
                "no-alert": 1,
                "no-else-return": 1,
                "no-eval": 1,
                "no-implied-eval": 1,
                "no-invalid-this": 1,
                "no-undef-init": 1,
                "no-undefined": 1,
                "no-use-before-define": 1,
                "arrow-parens": [1, "always"],
                "arrow-spacing": 1,
                "brace-style": 1,
                "camelcase": [1, {"properties": "always"}],
                "comma-spacing": 1,
                "comma-style": 1,
                "constructor-super": 1,
                "eol-last": 1,
                "indent": ["error", 2],
                "linebreak-style": [1, "unix"],
                "new-parens": 1,
                "no-array-constructor": 1,
                "no-class-assign": 1,
                "no-const-assign": 1,
                "no-this-before-super": 1,
                "no-trailing-spaces": 1,
                "no-var": 1,
                "prefer-const": 1,
                "prefer-reflect": 1,
                "prefer-spread": 1,
                "quotes": [1, "single"],
                "valid-jsdoc": 1
              }
            }
          }
        ]
      },
      {
        test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
        use: 'url-loader'
      }
    ]
  },
  plugins: [
    new webpack.optimize.ModuleConcatenationPlugin(),
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: 'html/index.html'
    })
  ]
};
