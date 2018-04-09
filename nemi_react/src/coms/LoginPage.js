import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom'
import Cookies from 'js-cookie'
import { Form, Icon, Input, Button, Checkbox, Layout, message } from 'antd';

import { userLogin } from '../apis/login'
import { NProgress } from '../utills/loading'

import Nemiicon from '../img/Ant.svg'
import '../css/login.css';


class Login extends Component {
  state = {
      load: true,
      username: {
        value: '',
        error: ''
      },
      password: {
        value: '',
        error: ''
      }
    }

  ChangeLogin = (e, type) => {
      e.preventDefault();
      let obj={};
      obj[type] = {
          value: e.target.value,
          error: ''
        }
      this.setState(obj);
  }
  handleSubmit = (e) => {
    e.preventDefault();
    if (!(this.state.username.value&&this.state.password.value)) {
      message.warning("输入账号密码先啊!");
      return false
    }
    this.setState({
      load: false
    });
    NProgress.start();
    userLogin({
      username: this.state.username.value,
      password: this.state.password.value
    }, this)
  }

  componentWillMount(){
    const { history } = this.props;
    if (Cookies.get("token")){
      NProgress.start();
      history.push("/")
    }else{
      NProgress.done();
    }
  }

  componentWillUpdate(nextProps, nextState) {
    NProgress.done();
    const { history } = this.props;
    if (Cookies.get("token")){
      NProgress.start();
      history.push("/")
    }else{
      NProgress.done();
    }
  }

  render() {
    return (
      <Layout className="login" type="flex" justify="center" align="middle">
        <Layout.Content>
          <div className="login-title">
            <span><img src={Nemiicon} alt=""/> Nemi 云存储系统</span>
            <p>解放移动存储设备，给您的数据以更安全的保障。</p>
          </div>
          <Form onSubmit={this.handleSubmit} className="login-form">
            <Form.Item
              hasFeedback
              validateStatus={this.state.username.error? "error":"success"}
              help={this.state.username.error}
              >
                <Input
                prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                placeholder="账户/邮箱"
                name="username"
                onChange={(e) => this.ChangeLogin(e, "username")}
                value={this.state.username.value}/>
            </Form.Item>
            <Form.Item
              hasFeedback
              validateStatus={this.state.password.error? "warning":this.state.username.error? "warning":"success"}
              help={this.state.password.error}
              >
                <Input
                prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                type="password"
                placeholder="密码"
                onChange={(e) => this.ChangeLogin(e, "password")}
                value={this.state.password.value}/>
            </Form.Item>
            <Form.Item>
              <Checkbox className="login-form-auto" checked={true}>自动登录</Checkbox>
              <Link className="login-form-forgot" to="">忘记密码</Link>
              <Button type="primary" htmlType="submit"
              loading={!this.state.load}
              className="login-form-button" >
                 登录
              </Button>
            </Form.Item>
          </Form>
        </Layout.Content>
        <Layout.Content>
          <div className="login-foot">
            <a>帮助</a>
            <a>隐私</a>
            <a>条款</a><br/>
            <p>Copyright©2018 All rights reserved Packet Inc.</p>
          </div>
        </Layout.Content>
      </Layout>
      )
  }
}

export default withRouter(Login);
