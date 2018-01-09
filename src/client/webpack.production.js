const HtmlWebpackPlugin = require('html-webpack-plugin');
const MinifyPlugin = require('babel-minify-webpack-plugin');
const common = require('./webpack.common.js');
const merge = require('webpack-merge');
const path = require('path');
const webpack = require('webpack');

module.exports = merge(common, {
  module: {
    rules: [
      {
        test: /\.css$/,
        include: [path.resolve(__dirname, 'css')],
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              minimize: true
            }
          }
        ]
      }
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }
    }),
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
});
