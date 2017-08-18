var http = require('http');
var fs = require('fs');
var exec = require('child_process').exec
var _ = require('underscore')
var Promise = require('bluebird')
var request = require('request')
Promise.config({ warnings: true, longStackTraces: true, cancellation: true, monitoring: true })

Object.defineProperty(Array.prototype,'_',{get(){return _(this)}, configurable:true})

var pad = (n, pad) => '0'.repeat((pad || 3)-(''+n).length)+n

var page_string = (i) => "arundel_ms_263_f"+pad(((i/2)|0)+1)+(i%2?"v":"r")

var get_url = (i, row, col, zoom) => 'http://www.bl.uk/manuscripts/Proxy.ashx?view='+page_string(i)+'_files/'+zoom+'/'+col+'_'+row+'.jpg'

var get_pages = (pages, rows, cols, zoom) => {
  try {fs.mkdirSync('results')} catch(e) {}
  return Promise.map(pages, x => get_page(x, rows, cols, zoom),{concurrency: 1}).all()
}

var get_page = (i, rows, cols, z) => {
  try {fs.mkdirSync('results/'+pad(i))} catch(e) {} // each page gets its own folder
  var q = rows.map(r => cols.map(c => [i, r, c, z]))._.flatten(true) // queue
  q = Promise.map(q, x => get_image(...x),{concurrency: 3}).all()  // q is a promise of an array now
  return q.then((p_arr) => {
    // console.log('in q.then')
    // console.log(p_arr)
    r = _.max(p_arr.map(x => x.r))
    c = _.max(p_arr.map(x => x.c))
    stitch_image(page_string(i), r, c, i)
    return true
  }).delay(5000)
}

var get_image = (i, row, col, zoom) => {
  var url = get_url(i, row, col, zoom)
  var path = 'results/'+pad(i)+'/'+page_string(i)+'_r'+pad(row)+'_c'+pad(col)+'.jpg'
  return download(url, path)
    .then(() => process_downloaded(path,i))
    .then(x => {console.log('download processed', x); return x})
    .delay(100)
}

var download = (url, path) => {
  // console.log('attempting download')
  console.log(url)
  var y = new Promise((res, err) => {
    request(url).pipe(fs.createWriteStream(path))
      .on('close', res)
      .on('error', e => {fs.unlink(path); err(e)})
      .on('er', e => {fs.unlink(path); err(e)})
    })
  return y
}

var process_downloaded = (path, i) => {
  // var p = path.match(/arundel_ms_263_f\d\d\d\w/)[0]
  var r = parseInt(path.match(/r\d+/)[0].slice(1))
  var c = parseInt(path.match(/c\d+/)[0].slice(1))
  if(fs.readFileSync(path).toString('utf8').slice(0, 5) === 'http:'){fs.unlinkSync(path); return {id: i, r: 0, c: 0}} // 404 error
  return {id: i, r: r, c: c}
}

var stitch_image = (page, rmax, cmax, i) => {
  console.log('stitch called for page no. '+i)
  exec('montage -geometry +0+0 '+
    '-tile '+(cmax+1)+'x'+(rmax+1)+ // dimensions
    ' results/'+pad(i)+'/*'+ // images to stitch
    ' results/'+pad(i)+'_'+page+'.jpg', // output file
    (error, stdout, stderr) => {
      [error,stdout,stderr].map(x => x && console.log('output/error: '+x))
    }
  )
}

var tall_pages = [_.range(34,40),_.range(48,60),156,157,168,169,_.range(184,194),_.range(250,258),295,296,297,_.range(300,308),_.range(368,374),384,385,398,399,412,413,418,419,420,421,426,427,446,447,460,461,462,463,560,561]._.flatten()

var too_big_pages = [83,158,159,182,183,238,239,240,241,242,243,248,249,290,291,292,293,294,295,296,298,299,312,313,314,315,374,375,378,379,380,381,386,387,388,389,438,439,440,441,451,456,498,499,502,512,513,514,515,516,517,519,520,521,522,523,540,541,542,543,544,545,546,547,553,554,555,562,563]

var normal_pages = _.range(0,580)._.difference(tall_pages)._.difference(too_big_pages)
// console.log(normal_pages)
Promise.resolve(true)
.then(() => get_pages(normal_pages,   _.range(7), _.range(9), 12))
.then(() => get_pages(tall_pages, _.range(14), _.range(9), 12)) 
.then(() => get_pages(too_big_pages, _.range(7),  _.range(9), 11))
