if (process.env.NODE_ENV === 'development') {
    module.exports = require('./client.dev')
} else {
    module.exports = require('./client.prod')
}
