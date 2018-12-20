import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'

import Button from 'components/Button'

import RotateSvg from '-!svg-react-loader!./rotate.svg'
import CopySvg from '-!svg-react-loader!./copy.svg'
import styles from './styles.scss'

const copyText = id => () => {
  document.getElementById(id).select()
  document.execCommand('copy')
}

const PhotoUrl = ({ photo, field, name, disabled }) => {
  const inputId = `photo${photo.id}${field}`
  const url = photo[field]
  return (
    <div
      className={styles.Photo__UrlLine}
    >
      <input
        type="text"
        value={url}
        id={inputId}
        className={styles.Photo__UrlInput}
      />
      <span
        className={styles.Photo__UrlName}
      >
        {name}
      </span>
      <a
        href={url}
        target={field}
      >
        {url}
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

class Photo extends PureComponent {

  static propTypes = {
    photo: PropTypes.shape({
      id: PropTypes.number.isRequired,
    }).isRequired,
    sizes: PropTypes.objectOf(PropTypes.string).isRequired,
    thumbField: PropTypes.string.isRequired,
    className: PropTypes.string,
    onClear: PropTypes.func.isRequired,
    onRotateLeft: PropTypes.func.isRequired,
    onRotateRight: PropTypes.func.isRequired,
    disabled: PropTypes.bool,
    messages: PropTypes.shape({
      clear: PropTypes.string.isRequired,
    }).isRequired,
  }

  static defaultProps = {
    disabled: false,
  }

  clearPhoto = () => {
    this.props.onClear(this.props.photo.id)
  }

  rotateLeft = () => {
    this.props.onRotateLeft(this.props.photo.id)
  }

  rotateRight = () => {
    this.props.onRotateRight(this.props.photo.id)
  }

  render() {
    return (
      <div
        className={classnames(styles.Photo, this.props.className)}
      >
        <div>
          <img
            className={styles.Photo__Img}
            src={this.props.photo[this.props.thumbField]}
          />
          <div
            className={styles.Photo__Actions}
          >
            <Button
              onClick={this.clearPhoto}
              disabled={this.props.disabled}
            >
              {this.props.messages.clear}
            </Button>
            <Button
              onClick={this.rotateLeft}
              disabled={this.props.disabled}
            >
              <RotateSvg
                height={15}
                fill="rgba(0, 0, 0, 0.4)"
                className={styles.flip}
              />
            </Button>
            <Button
              onClick={this.rotateRight}
              disabled={this.props.disabled}
            >
              <RotateSvg
                height={15}
                fill="rgba(0, 0, 0, 0.4)"
              />
            </Button>
          </div>
        </div>
        <div
          className={styles.Photo__Urls}
        >
          {Object.entries(this.props.sizes).map(([field, name]) => (
            <PhotoUrl
              key={field}
              field={field}
              name={name}
              photo={this.props.photo}
            />
          ))}
        </div>
      </div>
    )
  }
}

export default Photo
