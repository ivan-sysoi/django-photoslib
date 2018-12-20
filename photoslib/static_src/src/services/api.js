import axios from 'axios'

import cacheFactory from './memory-cache'

export default ({ getUrl, uploadUrl, rotateLeftUrl, rotateRightUrl, headers } = {}) => {
  const getPhotosCache = cacheFactory({ lifeTime: 0 })

  const processResponse = (response) => {
    if (response && 200 >= response.status < 300) {
      return response.data
    }
    throw new Error(`Invalid response status: ${response.statusText}`)
  }

  return {
    async get(idOrIds) {
      let ids
      if (Number.isInteger(idOrIds)) {
        ids = [idOrIds]
      } else {
        ids = Array.from(new Set(idOrIds.values()))
      }

      if (ids.length < 1) {
        return []
      }

      const cacheKey = ids.join('|')
      const results = getPhotosCache.get(cacheKey)
      if (results) {
        return results
      }
      return processResponse(await axios({
        url: `${getUrl}?ids=${ids.join(',')}`,
        headers,
        method: 'get',
      }))
    },

    async upload(file) {
      const formData = new FormData()
      formData.append('file', file)

      return processResponse(await axios({
        url: uploadUrl,
        method: 'post',
        headers,
        data: formData,
      }))
    },

    async rotateLeft(id) {
      return processResponse(await axios({
        url: rotateLeftUrl,
        method: 'post',
        headers,
        data: {
          ids: [id],
        },
      }))
    },

    async rotateRight(id) {
      return processResponse(await axios({
        url: rotateRightUrl,
        method: 'post',
        headers,
        data: {
          ids: [id],
        },
      }))
    },

  }
}
