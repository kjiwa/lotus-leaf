var gulp = require('gulp');
var browserify = require('gulp-browserify');
var eslint = require('gulp-eslint');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');

/**
 * A task that checks for syntactical and stylistic errors in JavaScript source
 * code.
 */
gulp.task('lint', function() {
  return gulp.src('src/**/*.js')
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError());
});

/**
 * A task that bundles the source code and its dependencies into a single file.
 * The file is not minified so that it can be more easily debugged during
 * development.
 */
gulp.task('package-dev', ['lint'], function() {
  return gulp.src('src/main.js')
    .pipe(browserify())
    .pipe(rename('uwsolar.js'))
    .pipe(gulp.dest('dist'));
});

/**
 * A task that bundles the source code and its dependencies into a single file
 * and minifies it.
 */
gulp.task('package', ['lint'], function() {
  return gulp.src('src/main.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(rename('uwsolar.js'))
    .pipe(gulp.dest('dist'));
});

/**
 * This task is the main entry point for Gulp. It creates a production package
 * from the source code.
 */
gulp.task('default', ['package']);
