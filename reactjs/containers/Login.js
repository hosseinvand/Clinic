import React, { Component, PropTypes } from 'react'
import axios from 'axios'
import { getFullUrl } from '../utils'

class Login extends Component {
    constructor() {
        super()
        this.state = {
            username: '',
            password: ''
        }
    }

    login() {
        axios.post(getFullUrl("login/"), {username: this.state.username, password: this.state.password}).then(
            function (response) {
                console.log(response)
            },
            function (error) {
                console.log(error)
            }
        )
    }

    render() {
        return (
                <div className="col-md-4 col-md-offset-4">
                    <div className="panel panel-default">
                        <div className="panel-body">
                            <form name="searchForm" className="form-horizontal" method="post">
                                <fieldset>
                                    <div className="form-group">
                                        <div className="col-xs-10 col-xs-offset-1">
                                        <input className="form-control" id="id_username"
                                               value={this.state.username}
                                               onChange={event => this.setState({username: event.target.value})}
                                               maxLength="150" name="username" placeholder="نام کاربری" type="text" required />
                                        </div>
                                    </div>
                                    <div className="form-group">
                                        <div className="col-xs-10 col-xs-offset-1">
                                        <input className="form-control" id="id_password"
                                               value={this.state.password}
                                               onChange={event => this.setState({password: event.target.value})}
                                               name="password" placeholder="رمز عبور" type="password" required />
                                        </div>
                                    </div>
                                    <div className="form-group">
                                        <div className="col-xs-10 col-xs-offset-1">
                                            <div type="submit" className="btn btn-lg btn-block btn-raised btn-primary" onClick={this.login.bind(this)}>
                                                ورود
                                            </div>
                                        </div>
                                    </div>
                                </fieldset>
                            </form>
                        </div>
                    </div>
                </div>
        )
    }
}

export default Login