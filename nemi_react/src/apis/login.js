import axios from 'axios'
import Cookies from 'js-cookie'

import { NEMI_URL } from './config'

import { message } from 'antd';

let userLogin = (body, thisApp) =>{
  axios.post(NEMI_URL + 'auth/login/', body).then(
    response => {
      Cookies.set("token", "Nemi "+response.data.data.token, { expires: 0.1 });
      thisApp.setState({
        username: {
          value: thisApp.state.username.value,
          error: ''
        },
        password: {
          value: thisApp.state.password.value,
          error: ''
        },
        load: true
      })
    }
  ).catch(
    error => {
      if (error.response) {
        thisApp.setState({
          username: {
            value: thisApp.state.username.value,
            error: error.response.data.message.username
          },
          password: {
            value: thisApp.state.password.value,
            error: error.response.data.message.password
          },
          load: true
        })
      } else {
        thisApp.setState({
          username: {
            value: thisApp.state.username.value,
            error: error
          },
          password: {
            value: thisApp.state.password.value,
            error: error
          },
          load: true
        })
      }
      message.error("有错误，请重新登录");
      Cookies.remove("token");
    }
  )
}

export {
    userLogin
};