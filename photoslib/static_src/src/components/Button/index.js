import React, { PureComponent, forwardRef } from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'

import buttonStyles from './styles.scss'


class Button extends PureComponent {
  static propTypes = {
    onClick: PropTypes.func,
    disabled: PropTypes.bool,
    buttonRef: PropTypes.func,
    preventDefault: PropTypes.bool,
    className: PropTypes.string,
    style: PropTypes.object,
    icon: PropTypes.element,
  }

  static defaultProps = {
    disabled: false,
    preventDefault: true,
  }

  onClick = (e) => {
    if (this.props.preventDefault) {
      e.preventDefault()
    }
    if (this.props.onClick) {
      this.props.onClick(e)
    }
  }

  render() {
    return (
      <button
        onClick={this.onClick}
        className={classnames(buttonStyles.Button, this.props.className)}
        disabled={this.props.disabled}
        ref={this.props.buttonRef}
        style={this.props.style}
      >
        {this.props.icon && (
          <span
            className={buttonStyles.Button__Icon}
          >
            {this.props.icon}
          </span>
        )}
        {this.props.children}
      </button>
    )
  }
}

export default forwardRef((props, ref) => <Button {...props} buttonRef={ref}/>)
