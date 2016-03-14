module.exports = {
  config: {
    files: {
      javascripts: {
        joinTo: {
          'libraries.js': /^(?!app\/)/,
          'app.js': /^app\//
        }
      },
      stylesheets: {
        joinTo: 'app.css'
      }
    }
  },
  plugins: {
    csscomb: {
      encoding: 'zen'
    },
    babel: {
      presets: ['es2015'],
      ignore: [/^(bower_components|vendor)/, 'app/legacyES5Code/**/*'],
      pattern: /\.(es6|jsx)$/
    },
    jshint: {},
    autoReload: {}
  }
};