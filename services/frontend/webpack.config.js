const webpack = require('webpack');
const HtmlWebPackPlugin = require('html-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

const path = require('path');

const CONFIG = require('./config/index');

const ENV_CONFIGS = CONFIG.ENV_CONFIGS;

function checkEnv(env) {
    if (Object.keys(ENV_CONFIGS).indexOf(env) === -1)
        throw new Error(`Unknown environment "${env}": use only "${Object.keys(ENV_CONFIGS).join(', ')}"`);
}

function checkEndpoint(endpoint) {
    if (Object.keys(ENV_CONFIGS).indexOf(endpoint) === -1)
        throw new Error(`Unknown endpoint "${endpoint}": use only "${Object.keys(ENV_CONFIGS).join(', ')}"`);
}

function isDevMode(env) {
    let devs = ['DEV', 'WORK'];
    return devs.indexOf(env) !== -1;
}

module.exports =  env => {
    const ENV = (env && Array.isArray(env.ENV))
        ? env.ENV.pop()
        : env && env.ENV || 'PRODUCTION';

    const ENDPOINT = env && env.ENDPOINT || ENV;

    const PATCH_VERSION = env && env.PATCH_VERSION || 0;

    //CHECK IS ENVIRONMENT AND ENDPOINT ARE ALLOWED
    checkEnv(ENV);
    checkEndpoint(ENDPOINT);

    console.log('Current environment is ', ENV,
        '; isDevMode = ', isDevMode(ENV),
        '; used ENDPOINT = ', ENDPOINT,
        '; PATCH_VERSION = ', PATCH_VERSION
    );

    return {
        mode: isDevMode(ENV) ? 'development' : 'production',
        devtool: isDevMode(ENV) ? 'source-maps' : false,
        entry: './src/index.js',
        output: {
            path: __dirname + '/dist',
            publicPath: '/',
            filename: 'bundle.js'
        },
        optimization: isDevMode(ENV) ? {} : {
            // minimize: true,
            // minimizer: [
            //     new TerserPlugin({
            //         parallel: true,
            //         cache: true,
            //         test: /\.js(\?.*)?$/i,
            //     }),
            // ],
            usedExports: true,
            sideEffects: true
        },
        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: require.resolve('babel-loader'),
                        options: {
                            presets: [['@babel/preset-env', {
                                targets: {
                                    browsers: 'last 2 versions',
                                },
                                modules: false
                            }], '@babel/preset-react'],
                            cacheDirectory: true,
                            plugins: ['react-hot-loader/babel'],
                        }
                    }
                },
                {
                    test: /\.html$/,
                    use: [
                        {
                            loader: 'html-loader',
                            options: {minimize: true}
                        }
                    ]
                },
                {
                    test: /\.(css|scss)$/,
                    use: [
                        {
                            loader: 'style-loader'
                        },
                        {
                            loader: 'css-loader'
                        },
                        {
                            loader: 'sass-loader'
                        }
                    ]
                },
                {
                    test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                    loader: 'url-loader?limit=10000&minetype=application/font-woff'
                },
                {
                    test: /\.(jpg|png|gif|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                    loader: 'file-loader'
                },
                {
                    test: /\.txt$/,
                    use: 'raw-loader'
                },
            ]
        },

        resolve: {
            extensions: ['*', '.js', '.jsx'],
            alias: {
                config: path.join(__dirname, 'src/config'),
            },
        },
        plugins: [
            // new TerserPlugin({
            //     parallel: true,
            //     terserOptions: {
            //         ecma: 6,
            //     },
            // }),
            new HtmlWebPackPlugin({
                template: './src/index.html',
                filename: './index.html',
                // favicon: './public/favicon.png',
            }),
            new webpack.DefinePlugin({
                '__APP__CONFIGURATION': JSON.stringify(CONFIG.makeConfig(ENV, ENDPOINT)),
                'process.env': {
                    'ENDPOINT': JSON.stringify(ENDPOINT),
                    'ENV': JSON.stringify(ENV),
                    'NODE_ENV': JSON.stringify(isDevMode(ENV) ? 'development' : 'production'),
                    'PATCH_VERSION': JSON.stringify(PATCH_VERSION),
                }
            }),
        ],
        devServer: {
            contentBase: './dist',
            host: '0.0.0.0',
            port: 8008,
            hot: true,
            historyApiFallback: true,
            disableHostCheck: true
        },
    };
};
