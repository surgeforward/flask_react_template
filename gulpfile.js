var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var less = require('gulp-less');
var minifyCSS = require('gulp-minify-css');
var browserify = require('browserify');
var es6ify = require('es6ify');
var reactify = require('reactify');
var source = require('vinyl-source-stream');
var streamify = require('gulp-streamify');
var sourcemaps = require('gulp-sourcemaps');

var paths = {
  scripts: './project/web/frontend/static/js/app.js',
  app_paths: './project/web/frontend/static/js/**/*.*',
  vendor_styles: 'project/web/frontend/static/css/*.css',
  styles: 'project/web/frontend/static/less/*.less'
};

gulp.task('scripts', function () {
    es6ify.traceurOverrides = {experimental: true};

    return browserify(paths.scripts)
        .transform(reactify)
        .transform(es6ify)
        .bundle()
        .pipe(source('app.js'))
        //.pipe(streamify(sourcemaps.init()))
            .pipe(streamify(concat('app.min.js')))
        //    .pipe(uglify())
        //.pipe(sourcemaps.write())
        .pipe(gulp.dest('project/web/frontend/static/dist/js'));
});

gulp.task('styles', function () {
    return gulp.src([paths.vendor_styles, paths.styles])
        .pipe(less())
        .pipe(concat('app.min.css'))
        .pipe(minifyCSS())
        .pipe(gulp.dest('project/web/frontend/static/dist/css'));
});

gulp.task('watch', function() {
  gulp.watch(paths.app_paths, ['scripts']);
  gulp.watch(paths.styles, ['styles']);
});


gulp.task('default', ['watch', 'scripts', 'styles']);
