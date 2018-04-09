import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Location from '../public/LocationPage'

import Cookies from 'js-cookie'
import {GetUserDisList, UserEnable, UserDestroy} from '../../apis/user'

import { NProgress } from '../../utills/loading'

import { Input, Row, Col, Icon, Tooltip, Button, Table } from 'antd';


class UserDisable extends Component {

  constructor(props) {
    super(props);
    let user_cookie = Cookies.get("user");
    this.state = {
        user: user_cookie?JSON.parse(user_cookie):false,
        selectedRowKeys: [],
        loading: false,
        filteredInfo: null,
        sortedInfo: null,
        filterDropdownVisible: false,
        searchText: '',

        data: []
    }
  }

  onSelectChange = (selectedRowKeys) => {
    console.log('selectedRowKeys changed: ', selectedRowKeys);
    this.setState({ selectedRowKeys });
  }

  handleChange = (pagination, filters, sorter) => {
    console.log('Various parameters', pagination, filters, sorter);
    this.setState({
      filteredInfo: filters,
      sortedInfo: sorter,
    });
  }

  clearAll = () => {
    this.setState({
      filteredInfo: null,
      sortedInfo: null,
      searchText: null,
    });
    this.flash_list()
  }
  onInputChange = (e) => {
    this.setState({ searchText: e.target.value });
  }
  onSearch = () => {
    const { searchText } = this.state;
    const reg = new RegExp(searchText, 'gi');
    this.setState({
      filterDropdownVisible: false,
      filtered: !!searchText,
      data: this.state.data.map((record) => {
        const match = record.username.match(reg);
        if (!match) {
          return null;
        }
        return {
          ...record,
          name: (
            <span>
              {record.username.split(reg).map((text, i) => (
                i > 0 ? [<span className="highlight" key={i}>{match[0]}</span>, text] : text
              ))}
            </span>
          ),
        };
      }).filter(record => !!record),
    });
  }

  flash_list=() =>{
    NProgress.start();
    GetUserDisList(this);
    NProgress.done();
  }

  componentDidMount(){
    this.flash_list()
  }

  enabled_user = (e, item) =>{
    e.preventDefault();
    UserEnable(this, item.id);
    this.flash_list()
  }

  destroy_user = (e, item) =>{
    e.preventDefault();
    UserDestroy(this, item.id);
    this.flash_list()
  }

  render() {
    const { selectedRowKeys } = this.state;
    const rowSelection = {
      selectedRowKeys,
      onChange: this.onSelectChange,
    };
    const hasSelected = selectedRowKeys.length > 0;
    let { sortedInfo } = this.state;
    sortedInfo = sortedInfo || {};
    const columns = [{
      title: '用户名',
      dataIndex: 'username',
      key: 'username',
      sorter: (a, b) => a.username.length - b.username.length,
      sortOrder: sortedInfo.columnKey === 'username' && sortedInfo.order,
      filterDropdown: (
        <div className="custom-filter-dropdown">
          <Input
            ref={ele => this.searchInput = ele}
            placeholder="Search name"
            value={this.state.searchText}
            onChange={this.onInputChange}
            onPressEnter={this.onSearch}
          />
          <Button type="primary" onClick={this.onSearch}>Search</Button>
        </div>
      ),
      filterIcon: <Icon type="smile-o" style={{ color: this.state.filtered ? '#108ee9' : '#aaa' }} />,
      filterDropdownVisible: this.state.filterDropdownVisible,
      onFilterDropdownVisibleChange: (visible) => {
        this.setState({
          filterDropdownVisible: visible,
        }, () => this.searchInput && this.searchInput.focus());
      },
      render: (text, record, index) => <a >
        {record.username+"("+record.email+")"}
      </a>
    },{
      title: '昵称',
      dataIndex: 'nickname',
      key: 'nickname'
    },{
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      sorter: (a, b) => a.role - b.role,
      sortOrder: sortedInfo.columnKey === 'role' && sortedInfo.order
    },{
      title: '操作',
      key: 'operation',
      render: (text, record, index) => <div>
        <Button type="primary" size="small" onClick={(e)=>this.enabled_user(e, record)}>恢复</Button>
        <span> </span>
        <Button type="danger" ghost size="small" onClick={(e)=>this.destroy_user(e, record)}>彻底删除</Button>
      </div>
    }];

    return (
      <div>
      <Location>
          <Row gutter={16} className="borad-header">
            <Col span={19}>
              <h3>超级管理员你好</h3>
              <span>你可以复活下面的用户哦</span>
            </Col>
            <Col span={5}>
              <div className="gutter-box">
                <div className="borad-header-inline">
                  <span className="text-gay">禁用数量</span><br/>
                  <Tooltip title="这么多可怜的人儿" placement="bottom" >
                    <h2>{this.state.data.length}<span className="text-gay text-small"> /200</span></h2>
                  </Tooltip>
                </div>
              </div>
            </Col>
          </Row>
        </Location>
        <div className="space-body">
          <div className="space-body-head">
            <Button type="primary" size="small" onClick={this.flash_list}>刷新</Button>
            <Button type="primary" size="small" onClick={this.clearAll}>清空筛选和排序</Button>
            <span style={{ marginLeft: 8 }}>
            {hasSelected ? `Selected ${selectedRowKeys.length} items` : ''}
          </span>
          </div>
          <Table
          rowSelection={rowSelection}
          columns={columns}
          loading={!this.state.load}
          onChange={this.handleChange}
          dataSource={this.state.data} />
        </div>
      </div>
    );
  }
}

export default withRouter(UserDisable);
