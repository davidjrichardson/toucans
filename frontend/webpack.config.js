const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
          {
            // Creates `style` nodes from JS strings
            loader: "style-loader",
          },
          {
            // Translates CSS into CommonJS
            loader: "css-loader",
          },
          {
            // Resolve URL includes
            loader: "resolve-url-loader",
          },
          {
            // Compiles Sass to CSS
            loader: "sass-loader",
            options: {
              sourceMap: true,
            },
          }
        ],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
    ]
  }
};