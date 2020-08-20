// const BrotliGzipPlugin = require('brotli-webpack-plugin');
// const CompressionPlugin = require('compression-webpack-plugin');
module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  // configureWebpack: {
  //   plugins: [
  //     new BrotliGzipPlugin({
  //         asset: '[path].br[query]',
  //         algorithm: 'br',
  //         test: /\.(js|css|html|svg)$/,
  //         threshold: 10240,
  //         minRatio: 0.8,
  //         quality: 11
  //     })
      // new CompressionPlugin({
      //   asset: '[path].gz[query]',
      //   test: /\.(js|css)$/,
      //   algorithm: 'gzip',
      //   threshold: 10240,
      //   minRatio: 0.8,
      //   // deleteOriginalAssets: true
      // })
  // ]
  // }
}