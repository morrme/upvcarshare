'use strict';
var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require("gulp-rename");
var uglify = require('gulp-uglify');
var beautify = require('gulp-beautify');
var gulpif = require('gulp-if');
var util = require('gulp-util');
var browserify = require('browserify');
var watchify = require('watchify');
var babelify = require('babelify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var imagemin = require('gulp-imagemin');

var config = require('./package.json');


// Helper for handle static paths
// -----------------------------------------------------------------------------
var pathsConfig = function (appName) {
  var app = appName || config.name;
  return {
    app: app,
    templates: app + '/templates',
    dist: {
      base: app + '/static/dist/',
      css: app + '/static/dist/css',
      fonts: app + '/static/dist/fonts',
      images: app + '/static/dist/img',
      js: app + '/static/dist/js'
    },
    src: {
      sass: app + '/static/src/sass',
      fonts: app + '/static/src/fonts',
      images: app + '/static/src/img',
      js: app + '/static/src/js'
    },
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
    gulp.src(pathsConfig().src.sass + '/project.scss')
      .pipe(sass(options).on('error', sass.logError))
      .pipe(rename('bundle.css'))
      .pipe(gulp.dest(pathsConfig().dist.css));
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

// Images Task
// -----------------------------------------------------------------------------
var imagesTask = function (options) {
  var run = function () {
    gulp.src(pathsConfig().src.images + '**/*')
      .pipe(imagemin())
      .pipe(gulp.dest(pathsConfig().dist.base));
  };

  // Run for development with watch
  if (options.development) {
    run();
    gulp.watch(options.watch, run);
    // Run for production with compressed
  } else {
    run();
  }
};

// Fonts Task
// -----------------------------------------------------------------------------
var fontsTask = function (options) {
  var run = function () {
    gulp.src(pathsConfig().src.fonts + '**/*')
      .pipe(gulp.dest(pathsConfig().dist.base));
  };

  // Run for development with watch
  if (options.development) {
    run();
    gulp.watch(options.watch, run);
    // Run for production with compressed
  } else {
    run();
  }
};

// App Task
// -----------------------------------------------------------------------------
// Task to build a bundle.js file with all the JavaScript code of the app,
// using browserify.
var appTask = function (options) {

  // App bundle creator
  var appBundler = browserify({
    entries: [options.src],
    transform: [babelify],
    debug: options.development,
    cache: {},
    packageCache: {},
    fullPaths: options.development
  });

  // The bundle process
  var bundle = function () {
    return appBundler.bundle()
      .on('error', util.log)
      .pipe(source('app.js'))
      .pipe(buffer())
      .pipe(gulpif(!options.development, uglify(), beautify()))
      .pipe(rename('bundle.js'))
      .pipe(gulp.dest(options.dist))
  };

  // Fire up watchify when developing
  if (options.development) {
    appBundler = watchify(appBundler);
    appBundler.on('update', bundle);
  }

  // Call to create bundle
  bundle();
};

// Default Task
// -----------------------------------------------------------------------------
// Starts our development workflow
gulp.task('default', function () {
  cssTask({
    watch: pathsConfig().src.sass + "/**/*.scss",
    development: true
  });
  appTask({
    src: pathsConfig().src.js + "/app.js",
    dist: pathsConfig().dist.js,
    development: true
  });
  imagesTask({
    development: false,
    watch: pathsConfig().src.images + "/**/*"
  });
  fontsTask({
    development: false,
    watch: pathsConfig().src.fonts + "/**/*"
  });
});

// Deploy Task
// -----------------------------------------------------------------------------
gulp.task('deploy', function () {
  cssTask({
    development: false
  });
  appTask({
    src: pathsConfig().src.js + "/app.js",
    dist: pathsConfig().dist.js,
    development: false
  });
  imagesTask({
    development: false
  });
  fontsTask({
    development: false
  });
});
