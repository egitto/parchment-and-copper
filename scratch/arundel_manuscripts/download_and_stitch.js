var http = require('http');
var fs = require('fs');
var exec = require('child_process').exec, child
var _ = require('underscore')
var rp = require('request-promise')

var download = (url,dest,cb)=>{
  console.log('attempting download')
  return rp(url).then((err,response)=>{
    console.log('url got')
    request(url).pipe(fs.createWriteStream(dest)).on('close', cb)
    return Promise.resolve(cb(dest))
  }).catch(e=>console.log(e))
}

var pad_int = (n,pad) => {
    return '0'.repeat((pad?pad:3)-(''+n).length)+n
}

var page_string = (i) =>{
  var n = pad_int(((i/2)|0)+1)
  return "arundel_ms_263_f"+n+(i%2?"v":"r")
}

var get_pages = (pages,rows,cols) => {
  if (pages.length === 0){return Promise.resolve(true)}
  get_page(page_string(pages[0]),rows,cols).then((p_arr)=>{
    r = _.max(p_arr.map(x=>x[1])) //these are supposed to be objects?? not arrays??
    c = _.max(p_arr.map(x=>x[2]))
    stitch_image(p_arr[0][0],r,c)
    return Promise.resolve(get_pages(pages.slice(1),rows,cols))
  }).catch(e=>console.log('get_pages error:'+e))
}

var get_page = (page_string,rows,cols) => {
  if (!fs.existsSync(page_string)){
    fs.mkdirSync(page_string)
  }
  console.log('get_page')
  var q = []
  _.range(rows).forEach(r=>_.range(cols).forEach(c=>q.push([page_string,r,c])))
  q = q.map(x=>get_image(...x))        // q should now be an array of promises
  return Promise.all(q).catch(e=>console.log('failure in Promise.all',e))
}

var get_image = (page_string,row,col) => {
  var url = 'http://www.bl.uk/manuscripts/Proxy.ashx?view='+page_string+'_files/13/'+col+'_'+row+'.jpg'
  var path = page_string+'/'+page_string.match(/f\d\d\d\w/)[0]+'_r'+pad_int(row)+'_c'+pad_int(col)+'.jpg'
  return download(url,path,process_downloaded)
}

var process_downloaded = (dest) => {
  var p = dest.match(/arundel_ms_263_f\d\d\d\w/)[0]
  var r = parseInt(dest.match(/r\d+/).slice(1))
  var c = parseInt(dest.match(/c\d+/).slice(1))
  var record = {id: p, r: r, c: c}
  if(fs.readFileSync(dest).toString('utf8').slice(0,5)==='http:'){fs.unlink(dest); return {id: p, r: 0, c: 0}} // 404 error
  return record
}

var stitch_image = (page,rmax,cmax) => {
  exec('montage -geometry +0+0 -tile '+(cmax+1)+'x'+(rmax+1)+' '+page+'/* '+page+'.jpg',
    function (error, stdout, stderr) {
      console.log('stdout: ' + stdout)
      console.log('stderr: ' + stderr)
      if (error !== null) {console.log('exec error: ' + error)}
    }
  )
}

// to get the entire image, you'll want get_pages([indicies,12,16])
// this is the second-highest resolution; for highest resolution, change '_files/13/' to 14
get_pages([1],2,2)

// console.log([2].map(page_string).forEach(page_string=>{
//   // get_page(page_string,12,16)
//   get_page(page_string,2,2)
// }))

// stitch_image('arundel_ms_263_f002v',2,2)

// stitch_image('arundel_ms_263_f001r',12,16)