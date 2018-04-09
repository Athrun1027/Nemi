import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({
    minimum: 0.01,
    easing: 'ease',
    speed: 500
});

const getFileSize = (byte_size) =>{
  if (byte_size > 1024) {
    if (byte_size > (1024*1024)) {
      if (byte_size > (1024*1024*1024)) {
        byte_size = Math.round(byte_size/(1024*1024*1024))
        return byte_size.toString() + "GB"
      }
      byte_size = Math.round(byte_size/(1024*1024))
      return byte_size.toString() + "MB"
    }
    byte_size = Math.round(byte_size/1024)
    return byte_size.toString() + "KB"
  }
  return byte_size.toString() + "B"
}

export {NProgress, getFileSize};