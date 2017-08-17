
throttle_test = () =>{
  var _ = require('underscore')
  var f = (x) => {
    console.log(x)
  }
  var g = _.throttle(f,12)
  [1,2,3,4,5,6].forEach(g)}

async function download_test() {
  var fs = require('fs')
  var http = require('http')
  var Promise = require('bluebird')
  var request = Promise.promisifyAll(require('request'))
  var url = 'http://www.qwantz.com/comics/comic2-3179.png'
  var path = 'quantz.png'
  console.log('requesting...')
  x = new Promise((resolve,reject)=>{
    request(url).pipe(fs.createWriteStream(path)).on('close',resolve).on('error',reject)
  })
  x.then((val)=>{console.log(val)})
}
download_test()