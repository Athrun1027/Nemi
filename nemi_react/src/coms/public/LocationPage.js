import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { Breadcrumb } from 'antd';

import '../../css/location.css';

const breadcrumbNameMap = {
  '/space': '存储空间',
  '/space/mine': '我的空间',
  '/space/group': '群组空间',
  '/space/search': '文件搜索',
  '/share': '文件分享',
  '/share/from': '我的分享',
  '/share/to': '分享给我',
  '/person': '个人设置',
  '/person/info': '信息修改',
  '/person/help': '系统帮助',
  '/person/logging': '查看日志',
  '/advanced': '回收站',
  '/advanced/user-disabled': '用户回收站',
  '/advanced/group-disabled': '群组回收站',
  '/advanced/file-disabled': '文件回收站',
  '/admin': '管理员',
  '/admin/user-admin': '用户管理',
  '/admin/group-admin': '群组管理'
};


class Location extends Component {
  state = {
    collapsed: false,
  };

  render() {
    const pathSnippets = this.props.location.pathname.split('/').filter(i => i);
    const extraBreadcrumbItems = pathSnippets.map((_, index) => {
      const url = `/${pathSnippets.slice(0, index + 1).join('/')}`;
      return (
        <Breadcrumb.Item key={url}>
          <Link to={url}>
            {breadcrumbNameMap[url]}
          </Link>
        </Breadcrumb.Item>
      );
    });
    const breadcrumbItems = [(
      <Breadcrumb.Item key="home">
        <Link to="/">Dashboard</Link>
      </Breadcrumb.Item>
    )].concat(extraBreadcrumbItems);
    return (
      <div className="bread-crumb">
        <Breadcrumb className="bread-body">
          {breadcrumbItems}
        </Breadcrumb>
        {this.props.children}
      </div>
    );
  }
}

export default withRouter(Location);
