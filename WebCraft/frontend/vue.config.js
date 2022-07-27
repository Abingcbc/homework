
module.exports = {
    publicPath: './',
    //配置跨域请求
    devServer: {
        host: 'localhost',
        port: 6270,    //启动端口号
        https: false,    //是否开启https
        hotOnly: false,
        proxy: { // 配置跨域
            '/api': {
                target: 'http://abingcbc.cn:10020',
                changOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    }
};
