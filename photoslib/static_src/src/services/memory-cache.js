import isString from 'lodash/isString'
import isInteger from 'lodash/isInteger'

export default ({ maxItems = 100, lifeTime = 300 * 1000 } = {}) => {
  const cache = new Map()

  function checkKey(key) {
    if (!isInteger(key) && !isString(key)) {
      throw new Error(`Cache key must be string or integer: ${key}`)
    }
  }

  function cutCache() {
    if (cache.size > maxItems) {
      const keysIter = cache.keys()
      while (cache.size > maxItems) {
        cache.remove(keysIter.next())
      }
    }
  }

  function getFromCache(key) {
    if (cache.has(key)) {
      const res = cache.get(key)
      if (res.timeout === 0 || res.timeout >= new Date().getTime()) {
        return res.data
      }
    }
  }

  function setIntoCache(key, data) {
    checkKey(key)
    cutCache()
    cache.set(key, {
      timeout: lifeTime > 0 ? new Date().getTime() + lifeTime : 0,
      data
    })
  }

  return {
    get: getFromCache,
    set: setIntoCache,
  }

}
