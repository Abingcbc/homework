
module.exports = {
    publicPath: './',
    //配置跨域请求
    devServer: {
        host: 'localhost',
        port: 8080,    //启动端口号
        https: false,    //是否开启https
        hotOnly: false,
        proxy: { // 配置跨域
            '/api': {
                target: 'http://localhost:11000/api',
                changOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            },
            '/image': {
                target: 'https://sm.ms/api/v2',
                changOrigin: true,
                pathRewrite: {
                    '^/image': ''
                }
            },
            '/server': {
                target: 'http://localhost:13000/api',
                changOrigin: true,
                pathRewrite: {
                    '^/server': ''
                }
            }
        }
    }
};
