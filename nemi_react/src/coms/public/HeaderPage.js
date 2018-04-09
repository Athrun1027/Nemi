import React, { Component } from 'react';
import Cookies from 'js-cookie'
import { withRouter, Link } from 'react-router-dom'

import { Layout, Menu, Icon, Avatar, Dropdown, message } from 'antd';

import NoticeIcon from 'ant-design-pro/lib/NoticeIcon';

import {MessageNotRead} from '../../apis/message'

import { NProgress } from '../../utills/loading'
import '../../css/headerbar.css';


class HeaderBar extends Component {

  constructor(props) {
      super(props);
      let user_cookie = Cookies.get("user");
      this.state = {
          user: user_cookie?JSON.parse(user_cookie):false,
          load: false,
          data: []
      }
  }

  logout = ({key, keyPath})=>{
    NProgress.start();
    if (key === "4"){
      Cookies.remove("token");
      this.props.history.push("/login")
    }
    if (key === "1"){
      this.props.history.push("/person/info")
    }
    if (key === "2"){
      this.props.history.push("/person/logging")
    }
  }

  confirm = (e) => {
    e.preventDefault();
    message.success('Click on Yes');
  }

  cancel = (e) => {
    e.preventDefault();
    message.error('Click on No');
  }

  componentDidMount(){
    NProgress.start();
    MessageNotRead(this);
    NProgress.done();
  }

  render() {
    const menu = (
          <Menu onClick={this.logout}>
            <Menu.Item key="1">
              <Icon type="user" /> 个人中心
            </Menu.Item>
            <Menu.Item key="2">
              <Icon type="setting" /> 设置
            </Menu.Item>
            <Menu.Divider />
            <Menu.Item key="4" style={{color:"red"}}>
              <Icon type="logout" /> 退出登录
            </Menu.Item>
          </Menu>
        );
    return (
        <Layout.Header style={
          { background: '#fff', padding: 0, overflow: 'hidden', boxShadow: '0 1px 4px rgba(0,21,41,.08)', position: 'relative' }
        }>
          <Icon
            className="home-trigger"
            type={this.props.collapsed ? 'menu-unfold' : 'menu-fold'}
            onClick={this.props.toggle}
          />
          <div className="home-user">
            <div className="home-hover">
              <Link to="/space/search" >
                <Icon type="search" style={{ fontSize: 18 }} />
              </Link>
            </div>
            <div className="home-hover">
            <Link to="/person/help" >
              <Icon type="question-circle-o" style={{ fontSize: 18 }} />
            </Link>
            </div>
            <div className="home-hover">
              <NoticeIcon
                className="notice-icon"
                count={this.state.data.length}
                loading={false}
                onItemClick={(item, tabProps) => {console.log(item, tabProps)}}
                onClear={(tabTitle) => this.setState({
                  "data": []
                })}
                popupAlign={{ offset: [20, -16] }}
              >
                <NoticeIcon.Tab
                  list={this.state.data}
                  title="消息"
                  emptyText="您已读完所有消息"
                  emptyImage="https://gw.alipayobjects.com/zos/rmsportal/sAuJeJzSKbUmHfBQRzmZ.svg"
                />
              </NoticeIcon>
            </div>
            <div className="home-hover">
            <Dropdown overlay={menu} placement="bottomRight">
                <a>
                  <Avatar className="home-user-avatar"
                    src={this.state.user.img_url}
                  />
                  <span>{this.state.user.nickname}</span>
                </a>
            </Dropdown>
            </div>
          </div>
        </Layout.Header>
    )
  }
}

export default withRouter(HeaderBar);