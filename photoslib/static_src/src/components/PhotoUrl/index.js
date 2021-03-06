import React from 'react'
import PropTypes from 'prop-types'

import Button from 'components/Button'

import CopySvg from '-!svg-react-loader!./copy.svg'
import styles from './styles.scss'

const copyText = id => () => {
  document.getElementById(id).select()
  document.execCommand('copy')
}

const cutUrl = (url) => {
  if (url.length > 30) {
    return `${url.slice(0, 12)}...${url.slice(-15)}`
  }
  return url
}

const PhotoUrl = ({ id, url, name, disabled }) => {
  const inputId = `photo${id}`
  return (
    <div
      className={styles.PhotoUrl}
    >
      <input
        type="text"
        value={url}
        id={inputId}
        className={styles.PhotoUrl__Input}
      />
      <span
        className={styles.PhotoUrl__Name}
      >
        {name}
      </span>
      <a
        href={url}
        target={id}
      >
        {cutUrl(url)}
      </a>
      <Button
        onClick={copyText(inputId)}
        disabled={disabled}
      >
        <CopySvg
          height={12}
          fill="rgba(0, 0, 0, 0.4)"
        />
      </Button>
    </div>
  )
}

PhotoUrl.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
  disabled: PropTypes.bool,
}

PhotoUrl.defaultProps = {
  disabled: false,
}

export default PhotoUrl
