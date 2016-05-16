'use strict';
var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require("gulp-rename");
var config = require('./package.json');

// Helper for handle static paths
// -----------------------------------------------------------------------------
var pathsConfig = function (appName) {
  var app = appName || config.name;
  return {
      app: app,
      templates: app + '/templates',
      css: app + '/static/css',
      sass: app + '/static/sass',
      fonts: app + '/static/fonts',
      images: app + '/static/images',
      js: app + '/static/js',
      manageScript: app + 'manage.py'
    }
};


// CSS Task
// -----------------------------------------------------------------------------
var cssTask = function (options) {

  // Default include node_modules to SASS include paths
  var sassOptions = {
    includePaths: ['./node_modules/'],
    errLogToConsole: true
  };

  // Common 'run' code for each options
  var run = function (options) {
    options = sassOptions || options;
    gulp.src(pathsConfig().sass + '/project.scss')
      .pipe(sass(options).on('error', sass.logError))
      .pipe(rename('bundle.css'))
      .pipe(gulp.dest(pathsConfig().css));
  };

  // Run for development with watch
  if (options.development) {
    run();
    gulp.watch(options.watch, run);
  // Run for production with compressed
  } else {
    run({outputStyle: 'compressed'});
  }

};

// Default Task
// -----------------------------------------------------------------------------
// Starts our development workflow
gulp.task('default', function () {
  cssTask({
    development: true,
    watch: pathsConfig().sass + "/**/*.scss"
  })
});

// Deploy Task
// -----------------------------------------------------------------------------
gulp.task('deploy', function () {
  cssTask({
    development: false
  })
});
