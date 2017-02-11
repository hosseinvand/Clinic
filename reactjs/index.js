import React from 'react'
import ReactDOM from 'react-dom'

const Hello = React.createClass ({
    render: function() {
        return (
            <h1>
            Hello, React! Testing
            </h1>
        )
    }
})

ReactDOM.render(<Hello />, document.getElementById('container'))