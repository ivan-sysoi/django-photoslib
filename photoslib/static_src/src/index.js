import React from 'react'
import ReactDOM from 'react-dom'

import createPhotosApi from './services/api'
import App from './App'

window.__photoslibInit = ({ rootElement, inputName, messages, apiOptions, opts, initialValue }) => {
  const headers = (() => {
    const value = `; ${document.cookie}`
    const parts = value.split('; csrftoken=')
    return {
      'X-CSRFToken': parts.pop().split(';').shift(),
    }
  })()

  ReactDOM.render((
    <App
      inputName={inputName}
      photosApi={createPhotosApi({ ...apiOptions, headers })}
      opts={opts}
      messages={messages}
      initialValue={Number.isInteger(initialValue)
        ? [initialValue]
        : (
          Array.isArray(initialValue)
            ? initialValue
            : []
        )}
    />
  ), rootElement)

  return function successCallback(callback) {
    callback()
  }
}
