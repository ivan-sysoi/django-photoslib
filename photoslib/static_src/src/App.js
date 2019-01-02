import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import Dropzone from 'react-dropzone'
import HTML5Backend from 'react-dnd-html5-backend'
import { DragDropContext } from 'react-dnd'

import Button from 'components/Button'
import PhotosList from 'components/PhotosList'
import Spinner from 'components/Spinner'

import styles from './styles.scss'
import UploadSvg from '-!svg-react-loader!./upload.svg'


class App extends PureComponent {
  static propTypes = {
    input: PropTypes.instanceOf(HTMLElement).isRequired,
    photosApi: PropTypes.object.isRequired,
    value: PropTypes.oneOfType([PropTypes.number, PropTypes.arrayOf(PropTypes.number)]),
    messages: PropTypes.shape({
      upload: PropTypes.string.isRequired,
      uploadError: PropTypes.string.isRequired,
      criticalError: PropTypes.string.isRequired,
    }).isRequired,
    opts: PropTypes.shape({
      appId: PropTypes.string.isRequired,
      maxSize: PropTypes.number.isRequired,
      multiply: PropTypes.bool.isRequired,
      sortable: PropTypes.bool.isRequired,
      sizeNames: PropTypes.object.isRequired,
    }).isRequired,
  }

  static defaultProps = {}

  state = {
    photos: [],
    loading: false,
    criticalError: false,
    errorInd: 0,
    errors: [],
  }

  updateInputValue = () => {
    if (this.props.opts.multiply) {
      this.props.input.value = this.state.photos.map(p => p.id).join(',')
    } else {
      this.props.input.value = this.state.photos.length > 0 ? this.state.photos[0].id : ''
    }
  }

  componentDidMount() {
    let ids
    if (Number.isInteger(this.props.value)) {
      ids = [this.props.value]
    } else if (Array.isArray(this.props.value) && this.props.value.length > 0) {
      ids = this.props.value
    }

    if (ids) {
      this.setState({ loading: true })
      this.props.photosApi
        .get(ids)
        .then((photos) => {
          this.setState({
            photos,
            loading: false,
          }, () => {
            this.updateInputValue()
          })
        }, (err) => {
          console.error(err)
          this.setState({ criticalError: true, loading: false })
        })
    }
  }

  addError = (mess) => {
    this.setState(prevState => ({
      ...prevState,
      errorInd: prevState.errorInd + 1,
      errors: [
        ...prevState.errors,
        { mess, key: prevState.errorInd },
      ],
    }), () => {
      setTimeout(() => {
        this.setState(prevState => ({
          ...prevState,
          errors: prevState.errors.slice(1),
        }))
      }, 8000)
    })
  }

  uploadPhoto = (file) => {
    this.setState({ loading: true })
    this.props.photosApi.upload(file)
      .then(photo => {
        if (!this.state.photos.find(p => p.id === photo.id)) {
          this.setState(prevState => ({
            photos: [
              ...prevState.photos,
              photo,
            ],
            loading: false,
          }), () => {
            this.updateInputValue()
          })
        }
      }, (err) => {
        console.error(err)
        this.addError(this.props.messages.uploadError)
        this.setState({ loading: false })
      })
  }

  onDrop = (files) => {
    files.map(this.uploadPhoto)
  }

  onClearPhoto = (id) => {
    this.setState(prevState => ({
      photos: prevState.photos.filter(p => p.id !== id),
    }), () => {
      this.updateInputValue()
    })
  }

  rotate = (left) => {
    const apiMeth = left ? this.props.photosApi.rotateLeft : this.props.photosApi.rotateRight
    return (id) => {
      const photoInd = this.state.photos.findIndex(p => p.id === id)
      if (photoInd !== -1) {
        this.setState({ loading: true })
        apiMeth(id)
          .then((photo) => {
            this.setState(prevState => {
              const photos = prevState.photos
              photos[photoInd] = photo
              return {
                photos: [
                  ...photos,
                ],
                loading: false,
              }
            }, () => {
              this.updateInputValue()
            })
          }, (err) => {
            console.error(err)
            this.setState({ loading: false })
          })
      }
    }
  }

  onRotateLeft = this.rotate(true)
  onRotateRight = this.rotate(false)

  onReorder = (startIndex, endIndex) => {
    this.setState((prevState) => {
      const newPhotos = [...prevState.photos]
      const [removed] = newPhotos.splice(startIndex, 1)
      newPhotos.splice(endIndex, 0, removed)
      return {
        photos: newPhotos,
      }
    }, () => {
      this.updateInputValue()
    })
  }

  render() {
    if (this.state.criticalError) {
      return this.props.messages.criticalError
    }

    return (
      <div
        className={styles.PhotoField}
      >
        <PhotosList
          appId={this.props.opts.appId}
          photos={this.state.photos}
          onReorder={this.onReorder}
          onClear={this.onClearPhoto}
          onRotateLeft={this.onRotateLeft}
          onRotateRight={this.onRotateRight}
          messages={this.props.messages}
          disabled={this.state.loading}
          sortable={this.props.opts.sortable}
          collapsible={this.props.opts.multiply}
          sizeNames={this.props.opts.sizeNames}
        />
        {this.state.loading && (<Spinner/>)}
        {(this.props.opts.multiply || this.state.photos.length === 0) && (
          <Dropzone
            onDrop={this.onDrop}
            accept="image/*"
            maxSize={this.props.opts.maxSize}
            multiple={this.props.opts.multiply}
            disabled={this.state.loading}
          >
            {(o) => (
              <div
                className={styles.PhotoField__UploadButton}
                {...o.getRootProps()}
              >
                <Button
                  onClick={o.open}
                  icon={<UploadSvg height={20} fill="rgba(0, 0, 0, 0.4)"/>}
                >
                  {this.props.messages.upload}
                </Button>
                <input {...o.getInputProps()} />
              </div>
            )}
          </Dropzone>
        )}
        {this.state.errors.length > 0 && (
          <ul
            className={styles.PhotoField__Errors}
          >
            {this.state.errors.map(({ mess, key }) => <li key={key}>{mess}</li>)}
          </ul>
        )}
      </div>
    )
  }
}

export default DragDropContext(HTML5Backend)(App)
