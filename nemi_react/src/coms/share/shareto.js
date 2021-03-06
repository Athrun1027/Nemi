import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Location from '../public/LocationPage'


import {ShareFileList} from '../../apis/share'
import Cookies from 'js-cookie'

import { NEMI_URL } from '../../apis/config'

import { NProgress, getFileSize } from '../../utills/loading'

import '../../css/space.css';

import { Input, Popconfirm, Progress, Row, Col, Icon, Tooltip, Button, Table } from 'antd';


const file_type = [
  "pdf", "ppt", "jpg", "markdown", "excel", "word"
]


class ShareTo extends Component {

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
        data_share_to: []
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
    this.flash_list(this.state.user.space_mine[0].root_folder.id)
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
        const match = record.object_name.match(reg);
        if (!match) {
          return null;
        }
        return {
          ...record,
          name: (
            <span>
              {record.object_name.split(reg).map((text, i) => (
                i > 0 ? [<span className="highlight" key={i}>{match[0]}</span>, text] : text
              ))}
            </span>
          ),
        };
      }).filter(record => !!record),
    });
  }

  flash_list=(id) =>{
    NProgress.start();
    ShareFileList(this)
    NProgress.done();
  }

  componentDidMount(){
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
      title: '名称',
      dataIndex: 'object_name',
      key: 'object_name',
      sorter: (a, b) => a.object_name.length - b.object_name.length,
      sortOrder: sortedInfo.columnKey === 'object_name' && sortedInfo.order,
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
      render: (text, record, index) => {
        let fileType = "file-text";
        if (file_type.indexOf(record.object_type) !== -1) {
          fileType = "file-" + record.object_type
        };
        if (record.object_type === "folder") {
          return <a onClick={(e)=>this.InFolder(e, record)}>
            <Icon type="folder" /> {text}
          </a>
        };
        return <a >
        <Icon type={fileType} /> {text}
      </a>
      }
    },{
      title: '原文件主人',
      key: 'creator',
      render: (text, record, index) => {
        return <a >{record.creator.creator_username+'('+record.creator.creator_nickname+')'}</a>
      }
    },{
      title: '下载',
      key: 'download',
      render: (text, record, index) => {
        if (record.object_type === "folder") {
          return <Icon type="minus" style={{ fontSize: 20}}/>
        };
        return <a href={NEMI_URL+"files/download/" + record.id}><Icon type="cloud-download-o" style={{ fontSize: 20}}/></a>
      }
    },{
      title: '大小',
      dataIndex: 'object_size',
      key: 'object_size',
      sorter: (a, b) => a.object_size - b.object_size,
      sortOrder: sortedInfo.columnKey === 'object_size' && sortedInfo.order,
      render: (text, record, index) => {
        if (record.object_type === "folder") {
          return <Icon type="minus" style={{ fontSize: 20}}/>
        };
        return <span>{getFileSize(text)}</span>
      }
    },{
      title: '操作',
      key: 'operation',
      render: (text, record, index) => <div>
        <Popconfirm placement="topRight" title="╥﹏╥…你竟然要删除别人给你的文件" onConfirm={(e)=>this.disabled_resource(e, record)} okText="删除" cancelText="算了">
          <Button type="danger" size="small">删除</Button>
        </Popconfirm>
      </div>
    }];

    return (
      <div>
      <Location>
          <Row gutter={16} className="borad-header">
            <Col span={17}>
              <h3>分享</h3>
              <span>这些是别人分享给你的文件</span>
            </Col>
            <Col span={7}>
              <div className="gutter-box">
                <div className="borad-header-inline">
                  <span className="text-gay">资源总数</span><br/>
                  <Tooltip title="嫌少？那没办法的" placement="bottom" >
                    <h2>{this.state.data_share_to.length}<span className="text-gay text-small"> /1000</span></h2>
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
          {this.state.upload?<Progress percent={this.state.upload}/>:""}
          <Table
          rowSelection={rowSelection}
          columns={columns}
          loading={!this.state.load}
          onChange={this.handleChange}
          dataSource={this.state.data_share_to} />
        </div>
      </div>
    );
  }
}

export default withRouter(ShareTo);
