import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom'

import { Layout, Menu, Icon } from 'antd';
import { NProgress } from '../../utills/loading'
import Cookies from 'js-cookie'

import Nemiicon from '../../img/Ant.svg'
import '../../css/siderbar.css';

const all_namespace = [
  "", "space", "share",
  "person", "setting",
  "advanced", "mine",
  "group","search",
  "info","parame",
  "help","logging",
  "from","to","user",
  "files","admin",
  "user-admin", "group-admin",
  "user-disabled", "group-disabled",
  "file-disabled"
]


class SiderBar extends Component {
  constructor(props) {
      super(props);
      let user_cookie = Cookies.get("user");
      user_cookie = user_cookie?JSON.parse(user_cookie):false
      let pathSnippets = this.props.location.pathname.split('/').filter(i => i);
      this.state = {
          user: user_cookie,
          pathname: this.props.location.pathname,
          openKeys: pathSnippets.length?pathSnippets:["dashboard"],
          selectKey: pathSnippets.length?pathSnippets[pathSnippets.length - 1]:"dashboard"
      }
  }

  state = {
    pathname: this.props.location.pathname,
    openKeys: ["dashboard"],
    selectKey: "dashboard"
  };

  OnClick = ({key, keyPath}) => {
    let url='';
    for (let index of keyPath.reverse()) {
      url += "/" + index
    }
    url = key==="dashboard"?"/":url;
    NProgress.start();
    this.props.history.push(url);
  }

  PathAvail = () => {
    let pathSnippets = this.props.location.pathname.split('/').filter(i => i);
    for (let index of pathSnippets) {
      if (all_namespace.indexOf(index) === -1) {
        NProgress.start();
        this.props.history.push("/404");
      }
    }
    if (this.props.location.pathname !== this.state.pathname) {
      NProgress.start();
      if (pathSnippets.length === 0) {
        pathSnippets = ["dashboard"]
      }
      this.setState({
        pathname: this.props.location.pathname,
        openKeys: pathSnippets,
        selectKey: pathSnippets[pathSnippets.length - 1]
      })
    }else{
      NProgress.done();
    }
  }

  onOpenChange = (openKeys) => {
    this.setState({
      openKeys: [openKeys[openKeys.length - 1]]
    })
  }


  // componentWillMount(){
  //   console.log("componentWillMount");
  //   console.log("this.props.location",this.props.location);
  //   // this.PathAvail();
  // }
  // componentWillUpdate(nextProps, nextState) {
  //   console.log("componentWillUpdate");
  //   console.log("this.props.location",this.props.location);
  //   // this.PathAvail();
  // }
  componentDidMount() {
    this.PathAvail();
  }
  componentDidUpdate(prevProps, prevState) {
    this.PathAvail();
  }

  render() {

    const admin_submenu1 = <Menu.SubMenu
              key="admin"
              title={<span><Icon type="api" /><span>管理员</span></span>}
            >
              <Menu.Item key="user-admin">用户管理</Menu.Item>
              <Menu.Item key="group-admin">群组管理</Menu.Item>
            </Menu.SubMenu>

    const admin_submenu2 = <Menu.SubMenu
              key="advanced"
              title={<span><Icon type="slack" /><span>回收站</span></span>}
            >
              <Menu.Item key="user-disabled">用户回收站</Menu.Item>
              <Menu.Item key="group-disabled">群组回收站</Menu.Item>
              <Menu.Item key="file-disabled">文件回收站</Menu.Item>
            </Menu.SubMenu>
    const admin_submenu3 = <Menu.SubMenu
              key="advanced"
              title={<span><Icon type="slack" /><span>回收站</span></span>}
            >
              <Menu.Item key="file-disabled">文件回收站</Menu.Item>
            </Menu.SubMenu>
    return (
        <Layout.Sider
          trigger={null}
          className="home-sider"
          collapsible
          collapsed={this.props.collapsed}
          width="256"
        >
          <div className="home-logo" >
            <Link to="">
              <img src={Nemiicon} alt=""/>
              <span>Nemi 云存储系统</span>
            </Link>
          </div>
          <Menu
          theme="dark"
          mode="inline"
          onClick={this.OnClick}
          onOpenChange={this.onOpenChange}
          openKeys={this.props.collapsed?[]:this.state.openKeys}
          selectedKeys={[this.state.selectKey]}
          >
            <Menu.Item key="dashboard">
                <Icon type="dashboard" />
                <span>dashboard</span>
            </Menu.Item>
            <Menu.SubMenu
              key="space"
              title={<span><Icon type="dropbox" /><span>存储空间</span></span>}
            >
              <Menu.Item key="mine">我的空间</Menu.Item>
              <Menu.Item key="group">群组空间</Menu.Item>
              <Menu.Item key="search">文件搜索</Menu.Item>
            </Menu.SubMenu>
            <Menu.SubMenu
              key="share"
              title={<span><Icon type="switcher" /><span>文件分享</span></span>}
            >
              <Menu.Item key="from">我分享的文件</Menu.Item>
              <Menu.Item key="to">分享给我的文件</Menu.Item>
            </Menu.SubMenu>
            <Menu.SubMenu
              key="person"
              title={<span><Icon type="setting" /><span>个人设置</span></span>}
            >
              <Menu.Item key="info">信息修改</Menu.Item>
              <Menu.Item key="help">系统帮助</Menu.Item>
              <Menu.Item key="logging">查看日志</Menu.Item>
            </Menu.SubMenu>
            {this.state.user.role === "admin"?admin_submenu1:""}
            {this.state.user.role === "admin"?admin_submenu2:admin_submenu3}
          </Menu>
        </Layout.Sider>
    )
  }
}

export default withRouter(SiderBar);