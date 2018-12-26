import React, { PureComponent, Fragment } from 'react'
import PropTypes from 'prop-types'
import Collapse from 'react-css-collapse'

import Photo from 'components/Photo'
import Button from 'components/Button'

import styles from './styles.scss'
import ArrowDownSvg from '-!svg-react-loader!./arrow-down.svg'

const getCLosed = (appId) => {
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
  }

  static defaultProps = {}

  state = {
    open: this.props.collapsible ? !getCLosed(this.props.appId) : true,
  }

  toggle = () => {
    this.setState(prevState => ({
      open: !prevState.open,
    }), () => {
      setOpened(this.props.appId, this.state.open)
    })
  }

  render() {
    const { photos, collapsible, messages, ...props } = this.props

    return (
      <Fragment>
        {this.props.collapsible && (
          <Button
            onClick={this.toggle}
            icon={<ArrowDownSvg
              height={18}
              fill="rgba(0, 0, 0, 0.4)"
              className={this.state.open && styles.flip}
            />}
          >
            {this.state.open ? messages.hide : messages.show}
          </Button>
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
