const common = require('./webpack.common.js');
const merge = require('webpack-merge');
const path = require('path');

module.exports = merge(common, {
  module: {
    rules: [
      {
        test: /\.css$/,
        include: [path.resolve(__dirname, 'css')],
        use: ['style-loader', 'css-loader']
      }
    ]
  },
});
