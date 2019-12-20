const path = require('path');

module.exports = {
  entry: './gnl/js/main.jsx',
  output: {
    path: path.join(__dirname, '/gnl/static/js/'),
    filename: 'bundle.js',
  },
  module: {
    loaders: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        exclude: /node_modules/, // add this line
        loader: 'babel-loader',
        query: {
          cacheDirectory: true,
          // Convert ES6 syntax to ES5 for browser compatibility
          presets: ['es2015', 'react'],
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};
