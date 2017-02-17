import React, { Component, PropTypes } from 'react'
import ReactDOM from 'react-dom'
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router'
import Login from './containers/Login'
import Layout from './containers/Layout'
import axios from 'axios'

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

class App extends Component {
    componentWillMount() {
        axios.interceptors.request.use(this.tokenInterceptor.bind(this))
        // axios.defaults.xsrfHeaderName = "X-CSRFToken";
        // axios.defaults.xsrfCookieName = 'csrftoken'
    }

    tokenInterceptor(config) {
        const csrftoken = getCookie('csrftoken');
        config.headers = {...config.headers, 'X-CSRFToken': csrftoken}
        return config
    }

    render() {
        return (
           <Router history={browserHistory}>
               <Route path="/notebook" component={Layout} >
                    <Route path="/notebook/login" component={Login} />
               </Route>
           </Router>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('container'))