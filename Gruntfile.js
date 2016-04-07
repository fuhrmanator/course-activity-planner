// https://raw.githubusercontent.com/lanmomo/lanmomo-website/master/Gruntfile.js

// The following job busts the browser cache by adding the md5 of the file in index.html
module.exports = function(grunt) {
    grunt.initConfig({
        copy: {
            pre: {
                files: [
                    {expand: true, cwd: 'public/', src: ['**'], dest: 'tmp/'}
                ]
            },
            post: {
                files: [
                    {expand: true, cwd: 'tmp/', src: ['**'], dest: 'static/'}
                ]
            }
        },
        cacheBust: {
            options: {
                encoding: 'utf8',
                algorithm: 'md5',
                length: 8
            },
            assets: {
                files: [{
                    src: ['tmp/index.html']
                }]
            }
        }
    });

    require('load-grunt-tasks')(grunt);
    grunt.registerTask('build', ['copy:pre',
                       'cacheBust',
                       'copy:post']);
};
