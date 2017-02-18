import React, {Component, PropTypes} from 'react'
import {Router, Route, Link, browserHistory, IndexRoute} from 'react-router'

class ErrorCard extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        const {
            error
        } = this.props

        return (
            <div className="col-md-8 col-md-offset-2">
                <div className="alert alert-danger text-center">
                    <strong>{error}</strong>
                </div>
            </div>
        )
    }
}

ErrorCard.propTypes = {
    error: PropTypes.string.isRequired,
}

export default ErrorCard
