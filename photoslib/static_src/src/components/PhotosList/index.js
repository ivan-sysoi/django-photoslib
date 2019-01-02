import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import Collapse from 'react-css-collapse'
import classnames from 'classnames'

import Photo from 'components/Photo'

import styles from './styles.scss'
import ArrowDownSvg from '-!svg-react-loader!./arrow-down.svg'

const getClosed = (appId) => {
  const key = `${appId}-collapsible`
  return localStorage.getItem(key) === '0'
}

const setOpened = (appId, collapsed) => {
  const key = `${appId}-collapsible`
  localStorage.setItem(key, collapsed ? '1' : '0')
}

class PhotosList extends PureComponent {
  static propTypes = {
    appId: PropTypes.string.isRequired,
    photos: PropTypes.arrayOf(PropTypes.shape({
      id: PropTypes.number.isRequired,
    })).isRequired,
    onReorder: PropTypes.func.isRequired,
    collapsible: PropTypes.bool.isRequired,
    messages: PropTypes.shape({
      count: PropTypes.string.isRequired,
    }).isRequired,
  }

  static defaultProps = {}

  state = {
    open: this.props.collapsible ? !getClosed(this.props.appId) : true,
  }

  toggle = () => {
    this.setState(prevState => ({
      open: !prevState.open,
    }), () => {
      setOpened(this.props.appId, this.state.open)
    })
  }

  render() {
    const { photos, collapsible, ...props } = this.props

    return (
      <Fragment>
        {collapsible && (
          <div
            className={styles.PhotosListHeader}
            onClick={this.toggle}
          >
            <ArrowDownSvg
              height={18}
              className={classnames(
                styles.PhotosListHeader__Icon,
                this.state.open && styles.PhotosListHeader__Icon_flip
              )}
            />
            <span>
              {this.props.messages.count}: {this.props.photos.length}
            </span>
          </div>
        )}
        <Collapse
          isOpen={this.state.open}
        >
          <div
            className={styles.PhotosList}
          >
            {photos.map((photo, ind) => (
              <Photo
                {...props}
                className={styles.PhotosList__Photo}
                key={photo.id}
                index={ind}
                photo={photo}
              />
            ))}
          </div>
        </Collapse>
      </Fragment>
    )
  }
}

export default PhotosList
