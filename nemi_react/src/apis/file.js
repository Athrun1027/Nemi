import axios from 'axios'
import Cookies from 'js-cookie'

import { NEMI_URL } from './config'

import { message } from 'antd';


let FileRecent = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'files/recent/',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        file_list: response.data.data,
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let ResourcesList = (thisApp, folder_id) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'resources/',{
    headers:{'Nemi-API-KEY': token},
    params:{
      PageSize:50,
      OrderBy:'-edit_time',
      Disable:0,
      folder_id:folder_id,
    }
  }).then(
    response => {
      response.data.data.forEach((item)=>{
        item["key"] = item["id"]
      })
      thisApp.setState({
        data: response.data.data,
        folder_id: folder_id,
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let ResourcesRoot = (thisApp, folder_id) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'resources/root/' + folder_id,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      let data_list = response.data.data.reverse()
      data_list[0].object_name = "根目录"
      thisApp.setState({
        folder_root: data_list,
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let ResourcesEdit = (thisApp, folder_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'resources/' + folder_id, put_data,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        edit_modal_visible: false,
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let FolderCreate = (thisApp, post_data) =>{
  let token = Cookies.get("token");
  axios.post(NEMI_URL + 'folders/', post_data,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        create_modal_visible: false,
        create_modal_text: '',
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let FolderTree = (thisApp, folder_id) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'folders/'+folder_id+'/tree/', {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        treeData: [response.data.data],
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let ResourcesMove = (thisApp, self_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'resources/'+self_id+'/move/', put_data,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        move_modal_visible: false,
        move_modal_select: "",
        move_modal_id: false,
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let ResourcesCopy = (thisApp, self_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'resources/'+self_id+'/copy/', put_data,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        copy_modal_visible: false,
        copy_modal_select: "",
        copy_modal_id: false,
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let ResourcesDisable = (thisApp, self_id) =>{
  let token = Cookies.get("token");
  axios.delete(NEMI_URL + 'resources/'+self_id,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let FileUpload = (thisApp, bucket_id) => {
    const { fileList } = thisApp.state;
    const formData = new FormData();
    fileList.forEach((file) => {
      formData.append(file.uid, file);
      formData.append(file.uid + "_size", file.size);
    });
    formData.append("folder_id", thisApp.state.folder_id);
    formData.append("bucket_id", bucket_id);
    let token = Cookies.get("token");
    axios.post(NEMI_URL + 'files/', formData,{
      headers:{'Nemi-API-KEY': token,'Content-Type': 'multipart/form-data'},
      onUploadProgress:(progressEvent)=>{
        let progress = Math.round(progressEvent.loaded / progressEvent.total * 100);
        thisApp.setState({
          uploading: true,
          upload: progress
        });
      }
    }).then(
      response => {
        thisApp.setState({
          defaultFileList: thisApp.state.defaultFileList.concat(thisApp.state.fileList),
          fileList: [],
          uploading: false,
          upload_modal_visible: false,
          upload: false
        });
        message.success('upload successfully.');
        thisApp.flash_list(thisApp.state.folder_id)
      }
    ).catch(
      error => {
        thisApp.setState({
          uploading: false,
        });
      }
    )
  }


let GetFileDisList = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'resources/dead/',{
    headers:{'Nemi-API-KEY': token},
    params:{
      PageSize:50,
      OrderBy:'-join_time',
      Disable:1
    }
  }).then(
    response => {
      response.data.data.forEach((item)=>{
        item["key"] = item["id"]
      })
      thisApp.setState({
        data:response.data.data,
        load: true
      })
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
    }
  )
}

let FileEnable = (thisApp, file_id) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'resources/'+file_id+'/enable/',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        load: true
      })
      message.success("恢复成功哦");
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      message.warning("恢复失败哦");
    }
  )
}

let FileDestroy = (thisApp, file_id) =>{
  let token = Cookies.get("token");
  axios.delete(NEMI_URL + 'resources/'+file_id+'/destroy/',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        load: true
      })
      message.success("彻底删除成功哦");
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      message.warning("彻底删除失败哦");
    }
  )
}


export {
  FileRecent,
  ResourcesList,
  ResourcesRoot,
  ResourcesEdit,
  FolderTree,
  ResourcesMove,
  ResourcesCopy,
  ResourcesDisable,
  FileUpload,
  GetFileDisList,
  FileEnable,
  FileDestroy,
  FolderCreate
};