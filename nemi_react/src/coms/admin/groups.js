import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Location from '../public/LocationPage'

import {GetGroupList, GroupCreate, GroupEdit, GroupDisable, GroupMemberSet} from '../../apis/group'
import Cookies from 'js-cookie'

import { NProgress } from '../../utills/loading'

import { Input, Modal, Transfer, Popconfirm, Row, Col, Icon, Tooltip, Button, Table } from 'antd';


class Group extends Component {

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
        filtered: false,

        edit_modal_visible: false,
        edit_nickname: "",
        edit_role: "",
        edit_modal_id: false,

        create_modal_visible: false,
        create_name: "",

        member_modal_visible: false,
        targetKeys: [],
        member_modal_id: false,

        fileList: [],
        defaultFileList: [],
        uploading: false,
        upload: false,

        treeData: [],
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
    GetGroupList(this, this.state.user.id);
    NProgress.done();
  }

  componentDidMount(){
    this.flash_list()
  }

  edit_modal_handleOk = (e) =>{
    e.preventDefault();
    let put_data = {
      nickname: this.state.edit_nickname,
      role: this.state.edit_role
    }
    GroupEdit(this, this.state.edit_modal_id, put_data)
    this.flash_list()
  }

  onChangeCreate = (e, value_type) => {
    e.preventDefault();
    let obj={};
    obj[value_type] = e.target.value;
    this.setState(obj);
  }
  create_modal_handleOk = (e) =>{
    e.preventDefault();
    let post_data = {
      name:this.state.create_name
    }
    GroupCreate(this, post_data)
    this.flash_list()
  }

  member_handleChange = (nextTargetKeys, direction, moveKeys) => {
    this.setState({ targetKeys: nextTargetKeys });
  }

  member_handleSelectChange = (sourceSelectedKeys, targetSelectedKeys) => {
    this.setState({ selectedKeys: [...sourceSelectedKeys, ...targetSelectedKeys] });
  }

  member_modal_handleOk = (e) =>{
    e.preventDefault();
    let put_data = {
      users:this.state.targetKeys,
    }
    GroupMemberSet(this, this.state.member_modal_id, put_data)
    this.flash_list()
  }

  disabled_user = (e, item) =>{
    e.preventDefault();
    GroupDisable(this, item.id);
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
      title: '群组名',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => a.name - b.name,
      sortOrder: sortedInfo.columnKey === 'name' && sortedInfo.order,
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
        {text}
      </a>
    },{
      title: '昵称',
      dataIndex: 'nickname',
      key: 'nickname'
    },{
      title: '成员人数',
      dataIndex: 'group_size',
      key: 'group_size',
      sorter: (a, b) => a.role - b.role,
      sortOrder: sortedInfo.columnKey === 'group_size' && sortedInfo.order,
      render: (text, record, index) => <a >
        {text+"/50"}
      </a>
    },{
      title: '操作',
      key: 'operation',
      render: (text, record, index) => <div>
        <Button type="primary" size="small" onClick={(e)=>this.setState({
            edit_modal_visible: true,
            edit_nickname: record.nickname,
            edit_role: record.role,
            edit_modal_id:record.id
          })}>编辑</Button>
        <span> </span>
        <Button type="primary" ghost size="small" onClick={(e)=>this.setState({
            member_modal_visible: true,
            member_modal_id:record.id,
            targetKeys:record.users.map(item => item.id)
          })}>成员</Button>
        <span> </span>
        <Popconfirm placement="topRight" title="╥﹏╥…确定要删除这个可爱的群组吗" onConfirm={(e)=>this.disabled_user(e, record)} okText="删除" cancelText="算了">
          <Button type="danger" size="small">删除</Button>
        </Popconfirm>
        <span> </span>
      </div>
    }];

    return (
      <div>
      <Location>
          <Row gutter={16} className="borad-header">
            <Col span={19}>
              <h3>管理员你好</h3>
              <span>请按照基本法来管理群组哦</span>
            </Col>
            <Col span={5}>
              <div className="gutter-box">
                <div className="borad-header-inline">
                  <span className="text-gay">群组总数</span><br/>
                  <Tooltip title="很抱歉，创建是有上限的" placement="bottom" >
                    <h2>{this.state.data.length}<span className="text-gay text-small"> /200</span></h2>
                  </Tooltip>
                </div>
              </div>
            </Col>
          </Row>
        </Location>
        <div className="space-body">
          <div className="space-body-head">
            <Button type="primary" size="small" onClick={()=>{this.flash_list(this.state.folder_id)}}>刷新</Button>
            <Button type="primary" size="small" onClick={()=>{this.setState({create_modal_visible: true})}}>新建群组</Button>
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
          <Modal
            title="修改信息"
            visible={this.state.edit_modal_visible}
            onOk={this.edit_modal_handleOk}
            onCancel={()=>{this.setState({edit_modal_visible: false})}}
          >
            <Input
              placeholder="请输入昵称"
              addonBefore="昵称"
              prefix={<Icon type="email" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_nickname}
              onChange={(e) => this.onChangeCreate(e, "edit_nickname")}
            />
          </Modal>
          <Modal
            title="新建群组"
            visible={this.state.create_modal_visible}
            onOk={this.create_modal_handleOk}
            onCancel={()=>{this.setState({create_modal_visible: false})}}
          >
            <Input
              placeholder="请输入群组名"
              addonBefore="群组名"
              prefix={<Icon type="email" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.create_name}
              onChange={(e) => this.onChangeCreate(e, "create_name")}
            />
          </Modal>
          <Modal
            title="修改成员"
            visible={this.state.member_modal_visible}
            onOk={this.member_modal_handleOk}
            onCancel={()=>{this.setState({member_modal_visible: false})}}
          >
            <Transfer
            dataSource={this.state.user.kids}
            titles={['可选', '已选']}
            targetKeys={this.state.targetKeys}
            onChange={this.member_handleChange}
            onSelectChange={this.member_handleSelectChange}
            render={item => item.nickname+'('+item.username+')'}
            rowKey={record => record.id}
            />
          </Modal>
          <Modal
            title="修改权限"
            visible={this.state.copy_modal_visible}
            onOk={this.copy_modal_handleOk}
            onCancel={()=>{this.setState({copy_modal_visible: false})}}
          >

          </Modal>
        </div>
      </div>
    );
  }
}

export default withRouter(Group);
