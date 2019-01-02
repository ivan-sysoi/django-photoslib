import React from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'

import styles from './styles.scss'

const inners = [0, 1, 2, 3].map(i => (
  <div
    key={i}
    className={[styles.Spinner__Inner, `${styles.Spinner__Inner}_${i}`].join(' ')}
  />
))

const Spinner = ({ className }) => (
  <div
    className={classnames(styles.Spinner, className)}
  >
    {inners}
  </div>
)

Spinner.propTypes = {
  className: PropTypes.string,
}

export default Spinner
