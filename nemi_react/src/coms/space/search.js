import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Location from '../public/LocationPage'

import {SearchFiles} from '../../apis/share'
import Cookies from 'js-cookie'

import { NEMI_URL } from '../../apis/config'

import { NProgress, getFileSize } from '../../utills/loading'

import '../../css/space.css';

import { Input, Radio, Row, Col, Icon, Button, Table } from 'antd';


const file_type = [
  "pdf", "ppt", "jpg", "markdown", "excel", "word"
]


class SpaceSearch extends Component {

  constructor(props) {
    super(props);
    let user_cookie = Cookies.get("user");
    this.state = {
        user: user_cookie?JSON.parse(user_cookie):false,
        selectedRowKeys: [],
        filteredInfo: null,
        sortedInfo: null,
        filterDropdownVisible: false,
        searchText: '',
        filtered: false,
        data: [],
        search_file_type: "all",
        search_space: "user",
        search_text: "",
        loading:false
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

  flash_list=(search_data) =>{
    if (search_data.search_text === "") {
      this.setState({
        loading: false
      });
      return true
    }
    NProgress.start();
    SearchFiles(this, search_data);
    NProgress.done();
  }

  onChangeCreate = (e, value_type) => {
    e.preventDefault();
    let obj={};
    obj[value_type] = e.target.value;
    this.setState(obj);
  }

  onButtonSearch = (e) => {
    e.preventDefault();
    this.setState({
      loading: true
    });
    this.flash_list({
      search_text: this.state.search_text,
      search_file_type: this.state.search_file_type,
      search_space: this.state.search_space,
    })
  }

  onChangeSearch = (e) => {
    e.preventDefault();
    this.setState({
      search_text:e.target.value,
      loading: true
    });
    this.flash_list({
      search_text: e.target.value,
      search_file_type: this.state.search_file_type,
      search_space: this.state.search_space,
    })
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
      title: '最近修改时间',
      dataIndex: 'edit_time',
      key: 'edit_time',
      sorter: (a, b) => Date.parse(new Date(a.edit_time)) - Date.parse(new Date(b.edit_time)),
      sortOrder: sortedInfo.columnKey === 'edit_time' && sortedInfo.order,
    }];

    const space = [
            { label: '我的空间', value: 'user' },
            { label: '群组空间', value: 'group' }
          ]
    const type = [
            { label: '所有', value: 'all' },
            { label: '文档', value: 'pdf' },
            { label: '图片', value: 'jpg' },
            { label: '笔记', value: 'markdown' },
          ]

    return (
      <div>
      <Location>
          <Row gutter={16} className="borad-header">
            <Col span={24}>
              <h3>文件搜索</h3>
            </Col>
          </Row>
          <Row gutter={16} className="borad-header">
            <Col span={4} />
            <Col span={12}>
              <Input
              placeholder="搜索内容键入会自动搜索......"
              prefix={<Icon type="search" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.search_text}
              onChange={(e) => this.onChangeSearch(e)}/>
            </Col>
            <Col span={4}>
              <Button
              loading={this.state.loading}
              type="primary" onClick={this.onButtonSearch}>搜索</Button>
            </Col>
            <Col span={4} />
          </Row>
          <Row gutter={16} className="borad-header">
            <Col span={4} />
            <Col span={20}>
              <div>
                <span>空间: </span>
                <Radio.Group options={space} onChange={(e)=>this.onChangeCreate(e, "search_space")} value={this.state.search_space} />
                <span>  文件类型: </span>
                <Radio.Group options={type} onChange={(e)=>this.onChangeCreate(e, "search_file_type")} value={this.state.search_file_type} />
              </div>
            </Col>
          </Row>
        </Location>
        <div className="space-body">
          <div className="space-body-head">
            <Button type="primary" size="small" onClick={this.clearAll}>清空筛选和排序</Button>
            <span style={{ marginLeft: 8 }}>
            {hasSelected ? `Selected ${selectedRowKeys.length} items` : ''}
          </span>
          </div>
          <Table
          rowSelection={rowSelection}
          columns={columns}
          loading={false}
          onChange={this.handleChange}
          dataSource={this.state.data} />
        </div>
      </div>
    );
  }
}

export default withRouter(SpaceSearch);
