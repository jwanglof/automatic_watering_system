"use strict";

var gulp = require('gulp'),
    sass = require('gulp-ruby-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    cssnano = require('gulp-cssnano'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    cache = require('gulp-cache'),
    livereload = require('gulp-livereload'),
    del = require('del');

gulp.task('styles', () => {
    return sass('./sass/**/*.scss', {style: 'expanded'})
        .pipe(autoprefixer('last 2 version'))
        //.pipe(gulp.dest('./static'))
        .pipe(concat('main.css'))
        .pipe(rename({suffix: '.min'}))
        .pipe(cssnano())
        .pipe(gulp.dest('./static'))
        .pipe(notify({message: 'SASS task complete!'}));
});

gulp.task('scripts', () => {
    return gulp.src('./javascript/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'))
        .pipe(concat('main.js'))
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest('./static'))
        .pipe(notify({message: 'Scripts task complete!'}));
});

gulp.task('clean', () => {
    return del(['./static']);
});

gulp.task('default', ['clean'], () => {
    gulp.start('styles', 'scripts');
});

gulp.task('watch', () => {
    // Watch .scss files
    gulp.watch('./sass/**/*.scss', ['styles']);

    gulp.watch('./javascript/**/*.js', ['scripts']);

    livereload.listen();

    gulp.watch(['./sass/**/*.scss', './javascript/**/*.js']).on('change', livereload.changed);
});