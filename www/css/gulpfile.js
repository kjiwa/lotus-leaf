var gulp = require('gulp');
var cleancss = require('gulp-clean-css');
var csslint = require('gulp-csslint');
var rename = require('gulp-rename');

/**
 * A task that checks for syntactical and stylistic errors in CSS source code.
 */
gulp.task('lint', function() {
  return gulp.src('src/**/*.css')
    .pipe(csslint())
    .pipe(csslint.formatter());
});

/**
 * A task that bundles the source code and its dependencies into a single file.
 * The file is not minified so that it can be more easily debugged during
 * development.
 */
gulp.task('package-dev', ['lint'], function() {
  return gulp.src('src/**/*.css')
    .pipe(rename('uwsolar.css'))
    .pipe(gulp.dest('dist'));
});

/**
 * A task that bundles the source code and its dependencies into a single file
 * and minifies it.
 */
gulp.task('package', ['lint'], function() {
  return gulp.src('src/**/*.css')
    .pipe(cleancss())
    .pipe(rename('uwsolar.css'))
    .pipe(gulp.dest('dist'));
});

/**
 * This task is the main entry point for Gulp. It creates a production package
 * from the source code.
 */
gulp.task('default', ['package']);
