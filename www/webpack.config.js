const HtmlWebpackPlugin = require('html-webpack-plugin');
const MinifyPlugin = require('babel-minify-webpack-plugin');
const webpack = require('webpack');

module.exports = env => {
  var args = {
    entry: './js/App.jsx',
    output: {
      path: __dirname + '/dist',
      filename: 'uwsolar.js'
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          exclude: /(node_modules|bower_components)/,
          use: [
            {
              loader: 'style-loader'
            },
            {
              loader: 'css-loader',
              options: {
                minimize: true
              }
            }
          ]
        },
        {
          test: /\.html$/,
          exclude: /(node_modules|bower_components)/,
          use: {
            loader: 'html-loader'
          }
        },
        {
          test: /\.jsx$/,
          exclude: /(node_modules|bower_components)/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-es2015', '@babel/preset-react']
            }
          }
        }
      ]
    },
    plugins: [
      new webpack.optimize.ModuleConcatenationPlugin(),
      new HtmlWebpackPlugin({
        filename: 'index.html',
        template: 'html/index.html',
        minify: {
          collapseBooleanAttributes: true,
          collapseWhitespace: true,
          removeAttributeQuotes: true,
          removeComments: true,
          removeEmptyAttributes: true,
          removeOptionalTags: true,
          removeRedundantAttributes: true,
          removeScriptTypeAttributes: true,
          removeStyleLinkTypeAttributes: true,
          removeTagWhitespace: true,
          useShortDoctype: true
        }
      }),
      new MinifyPlugin()
    ]
  };

  return args;
}
