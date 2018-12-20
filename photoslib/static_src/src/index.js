import React from 'react'
import ReactDOM from 'react-dom'

import createPhotosApi from './services/api'
import App from './App'


window.__photoslibInit = ({ rootElement, input, messages, apiOptions, opts, value }) => {
  const headers = (() => {
    const value = '; ' + document.cookie
    const parts = value.split('; csrftoken=')
    return {
      'X-CSRFToken': parts.pop().split(';').shift()
    }
  })()

  ReactDOM.render((
    <App
      input={input}
      photosApi={createPhotosApi({ ...apiOptions, headers })}
      opts={opts}
      messages={messages}
      value={value}
    />
  ), rootElement)
}
