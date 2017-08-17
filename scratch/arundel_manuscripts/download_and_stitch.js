var http = require('http');
var fs = require('fs');
var exec = require('child_process').exec, child
var _ = require('underscore')
var Promise = require('bluebird')
var request = require('request')
Promise.config({
    // Enable warnings
    warnings: true,
    // Enable long stack traces
    longStackTraces: true,
    // Enable cancellation
    cancellation: true,
    // Enable monitoring
    monitoring: true
});

Object.defineProperty(Array.prototype,'_',{get(){return _(this)}, configurable:true})

var pad_int = (n, pad) => {
    return '0'.repeat((pad?pad:3)-(''+n).length)+n
}

var page_string = (i) => {
  var n = pad_int(((i/2)|0)+1)
  return "arundel_ms_263_f"+n+(i%2?"v":"r")
}

var get_url = (page_string,row,col) => {
  return 'http://www.bl.uk/manuscripts/Proxy.ashx?view='+page_string+'_files/13/'+col+'_'+row+'.jpg'
}

var get_pages = (pages, rows, cols) => {
  return Promise.map(pages, (x) => get_page(page_string(x),rows,cols),{concurrency: 1})
}

var get_page = (page_string, rows, cols) => {
  try{fs.mkdirSync('results/'+page_string)}catch(e){} // each page gets its own folder
  q = _.range(rows).map(r => _.range(cols).map(c => [page_string, r, c]))._.flatten(true) // queue
  q = Promise.map(q, x => get_image(...x),{concurrency: 1}).all()  // q is a promise of an array now
  q = q.then((p_arr) => {
    console.log('in q.then')
    console.log(p_arr)
    r = _.max(p_arr.map(x => x.r))
    c = _.max(p_arr.map(x => x.c))
    stitch_image(p_arr[0].id, r, c)
    return true
  }).delay(5000)
  return q
}

var get_image = (page_string, row, col) => {
  var url = get_url(page_string,row,col)
  var path = 'results/'+page_string+'/'+page_string.match(/f\d\d\d\w/)[0]+'_r'+pad_int(row)+'_c'+pad_int(col)+'.jpg'
  y = download(url,path)
    .then(() => process_downloaded(path))
    .then((x) => {console.log('download processed',x); return x})
  return y
}

var download = (url, dest) => {
  console.log('attempting download')
  console.log(url)
  var y = new Promise((res,err) => {
    request(url).pipe(fs.createWriteStream(dest))
      .on('close', res)
      .on('error', (e) => {fs.unlink(dest); err(e)})
    })
  return y
}

var process_downloaded = (dest) => {
  var p = dest.match(/arundel_ms_263_f\d\d\d\w/)[0]
  console.log(dest,'processing downloaded image')
  var r = parseInt(dest.match(/r\d+/)[0].slice(1))
  var c = parseInt(dest.match(/c\d+/)[0].slice(1))
  var record = {id: p, r: r, c: c}
  if(fs.readFileSync(dest).toString('utf8').slice(0, 5) === 'http:'){fs.unlink(dest); return {id: p, r: 0, c: 0}} // 404 error
  return record
}

var stitch_image = (page, rmax, cmax) => {
  console.log('stitch called')
  exec('montage -geometry +0+0 -tile '+(cmax+1)+'x'+(rmax+1)+' results/'+page+'/* results/'+page+'.jpg',
    function (error, stdout, stderr) {
      console.log('stdout: ' + stdout)
      console.log('stderr: ' + stderr)
      if (error !== null) {console.log('exec error: ' + error)}
    }
  )
}

// to get the entire image, you'll want get_pages([indicies, 12, 16])
// this is the second-highest resolution; for highest resolution, change '_files/13/' to 14
get_pages(_.range(30), 12, 16)

// console.log([2].map(page_string).forEach(page_string => {
//   // get_page(page_string, 12, 16)
//   get_page(page_string, 2, 2)
// }))

// stitch_image('arundel_ms_263_f002v', 2, 2)

// stitch_image('arundel_ms_263_f001r', 12, 16)