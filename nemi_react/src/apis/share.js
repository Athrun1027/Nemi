import axios from 'axios'
import Cookies from 'js-cookie'

import { NEMI_URL } from './config'

import { message } from 'antd';


let ShareFile = (thisApp, post_data) =>{
  let token = Cookies.get("token");
  axios.post(NEMI_URL + 'shares/', post_data, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        share_modal_visible: false,
        share_targetKeys: [],
        share_modal_id: false,
        load: true
      })
      message.success("分享成功");
    }
  ).catch(
    error => {
      message.success("分享失败");
    }
  )
}

let ShareFileList = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'shares/', {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      response.data.share_from.forEach((item)=>{
        item["key"] = item["id"]
      })
      response.data.share_to.forEach((item)=>{
        item["key"] = item["id"]
      })
      thisApp.setState({
        data_share_from: response.data.share_from,
        data_share_to: response.data.share_to,
        load: true
      })
    }
  ).catch(
    error => {
      // message.success("分享失败");
    }
  )
}

let SearchFiles = (thisApp, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'search/', put_data, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      response.data.data.forEach((item)=>{
        item["key"] = item["id"]
      })
      thisApp.setState({
        data: response.data.data,
        loading: false
      })
    }
  ).catch(
    error => {
      thisApp.setState({
        data: [],
        loading: false
      })
    }
  )
}


export {
  ShareFile,
  SearchFiles,
  ShareFileList
};