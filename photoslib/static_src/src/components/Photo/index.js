import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'
import { DragSource, DropTarget } from 'react-dnd'

import Button from 'components/Button'
import PhotoUrl from 'components/PhotoUrl'

import RotateSvg from '-!svg-react-loader!./rotate.svg'
import DeleteSvg from '-!svg-react-loader!./delete.svg'
import styles from './styles.scss'

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
    sortable: PropTypes.bool.isRequired,
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
    const { connectDragPreview, connectDragSource, connectDropTarget, isDragging, sortable } = this.props

    return connectDragSource && connectDropTarget && connectDragPreview && connectDragSource(connectDropTarget(
      (
        <div
          className={classnames(
            styles.Photo,
            {
              [styles.Photo_dragging]: isDragging,
              [styles.Photo_sortable]: sortable,
            },
            this.props.className)}
        >
          <div>
            {connectDragPreview(
              <img
                className={styles.Photo__Img}
                src={this.props.photo[this.props.thumbField]}
              />
            )}
            <div
              className={styles.Photo__Actions}
            >
              <Button
                onClick={this.clearPhoto}
                disabled={this.props.disabled}
              >
                <DeleteSvg
                  height={15}
                  fill="rgba(0, 0, 0, 0.4)"
                />
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
    ))
  }
}

const PhotoType = 'Photo'

const targetPhotoSpec = {
  hover(props, monitor, component) {
    if (!component || !monitor.getItem().sortable) {
      return null
    }
    const dragIndex = monitor.getItem().index
    const hoverIndex = props.index

    if (dragIndex === hoverIndex) {
      return
    }
    props.onReorder(dragIndex, hoverIndex)
    monitor.getItem().index = hoverIndex
  },
}

const targetCollect = connect => ({ connectDropTarget: connect.dropTarget() })

const sourcePhotoSpec = {
  beginDrag(props) {
    return {
      index: props.index,
      sortable: props.sortable,
    }
  },
}
const sourcePhotoCollect = (connect, monitor) => {
  return {
    connectDragPreview: connect.dragPreview(),
    connectDragSource: connect.dragSource(),
    isDragging: monitor.isDragging(),
  }
}


export default DropTarget(
  PhotoType,
  targetPhotoSpec,
  targetCollect,
)(
  DragSource(
    PhotoType,
    sourcePhotoSpec,
    sourcePhotoCollect,
  )(Photo),
)
