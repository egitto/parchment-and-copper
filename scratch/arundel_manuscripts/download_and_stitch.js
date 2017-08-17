var http = require('http');
var fs = require('fs');
var exec = require('child_process').exec, child
var _ = require('underscore')
var Promise = require('bluebird')
var request = require('request')
Promise.config({ warnings: true, longStackTraces: true, cancellation: true, monitoring: true })

Object.defineProperty(Array.prototype,'_',{get(){return _(this)}, configurable:true})

var pad = (n, pad) => {
    return '0'.repeat((pad?pad:3)-(''+n).length)+n
}

var page_string = (i) => {
  var n = pad(((i/2)|0)+1)
  return "arundel_ms_263_f"+n+(i%2?"v":"r")
}

var get_url = (i, row, col, zoom) => {
  var ps = page_string(i)
  return 'http://www.bl.uk/manuscripts/Proxy.ashx?view='+ps+'_files/'+zoom+'/'+col+'_'+row+'.jpg'
}

var get_pages = (pages, rows, cols, zoom) => {
  try{fs.mkdirSync('results')}catch(e){}
  return Promise.map(pages, (x) => get_page(x, rows, cols, zoom),{concurrency: 1})
}

var get_page = (i, rows, cols, z) => {
  var ps = page_string(i)
  try{fs.mkdirSync('results/'+pad(i))}catch(e){} // each page gets its own folder
  var q = rows.map(r => cols.map(c => [i, r, c, z]))._.flatten(true) // queue
  q = Promise.map(q, x => get_image(...x),{concurrency: 3}).all()  // q is a promise of an array now
  q = q.then((p_arr) => {
    // console.log('in q.then')
    // console.log(p_arr)
    r = _.max(p_arr.map(x => x.r))
    c = _.max(p_arr.map(x => x.c))
    stitch_image(ps, r, c, i)
    return true
  }).delay(5000)
  return q
}

var get_image = (i, row, col, zoom) => {
  var url = get_url(i, row, col, zoom)
  var ps = page_string(i).match(/f\d\d\d\w/)[0]
  var path = 'results/'+pad(i)+'/'+page_string(i)+'_r'+pad(row)+'_c'+pad(col)+'.jpg'
  y = download(url, path)
    .then(() => process_downloaded(path,i))
    .then((x) => {console.log('download processed', x); return x})
    .delay(100)
  return y
}

var download = (url, path) => {
  // console.log('attempting download')
  console.log(url)
  var y = new Promise((res, err) => {
    request(url).pipe(fs.createWriteStream(path))
      .on('close', res)
      .on('error', (e) => {fs.unlink(path); err(e)})
    })
  return y
}

var process_downloaded = (path, i) => {
  // var p = path.match(/arundel_ms_263_f\d\d\d\w/)[0]
  var r = parseInt(path.match(/r\d+/)[0].slice(1))
  var c = parseInt(path.match(/c\d+/)[0].slice(1))
  var record = {id: i, r: r, c: c}
  if(fs.readFileSync(path).toString('utf8').slice(0, 5) === 'http:'){fs.unlinkSync(path); return {id: i, r: 0, c: 0}} // 404 error
  return record
}

var stitch_image = (page, rmax, cmax, i) => {
  console.log('stitch called for page no. '+i)
  exec('montage -geometry +0+0 '+
    '-tile '+(cmax+1)+'x'+(rmax+1)+ // dimensions
    ' results/'+pad(i)+'/*'+ // images to stitch
    ' results/'+pad(i)+'_'+page+'.jpg', // output file
    function (error, stdout, stderr) {
      stdout?console.log('stdout: ' + stdout):0
      stderr?console.log('stderr: ' + stderr):0
      if (error !== null) {console.log('exec error: ' + error)}
    }
  )
}

// to get the entire image, you'll want get_pages([indicies, 12, 16])
// get_pages(pagerange, rows, cols, zoom) zoom is from 1 to 14, recommend 13 for most pages. 
get_pages([30,31], _.range(4), _.range(4), 11)
// get_pages(_.range(15, 100), _.range(12), _.range(18), 13)

// console.log([2].map(page_string).forEach(page_string => {
//   // get_page(page_string, 12, 16)
//   get_page(page_string, 2, 2)
// }))

// stitch_image('arundel_ms_263_f002v', 2, 2)

// stitch_image('arundel_ms_263_f001r', 12, 16)