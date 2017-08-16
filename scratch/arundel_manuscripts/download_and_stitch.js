var http = require('http');
var fs = require('fs');
var exec = require('child_process').exec, child
var _ = require('underscore')

var download = function(url, dest, cb) {
  var file = fs.createWriteStream(dest);
  var request = http.get(url, function(response) {
    response.pipe(file);
    file.on('finish', function() {
      file.close();  // close() is async, call cb after close completes.
    });
  }).on('error', function(err) { // Handle errors
    fs.unlink(dest); // Delete the file async. (But we don't check the result)
    console.log(err,url,dest)
  }).on('finish', ()=>{
    console.log('Downloaded:',url);
    return Promise.resolve(cb(dest))});
  return Promise.resolve(request)
};

var pad_int = (n,pad) => {
    return '0'.repeat((pad?pad:3)-(''+n).length)+n
}

var page_string = (i) =>{
  var n = pad_int(((i/2)|0)+1)
  console.log(n.length)
  return "arundel_ms_263_f"+n+(i%2?"v":"r")
}

var get_pages = (pages,rows,cols) => {
  if (pages.length === 0){return}
  get_page(page_string(pages[0]),rows,cols).then((p_arr)=>{
    console.log(p_arr)
    r = _.max(p_arr.map(x=>x[1])) //these are supposed to be objects?? not arrays??
    c = _.max(p_arr.map(x=>x[2]))
    process_full_page(p_arr[0][0],r,c)
    get_pages(pages.slice(1),rows,cols)
  }).catch(e=>console.log('get_pages error:'+e))
}

var get_page = (page_string,rows,cols) => {
  if (!fs.existsSync(page_string)){
    fs.mkdirSync(page_string);
  }
  var q = []
  _.range(rows).forEach(r=>_.range(cols).forEach(c=>q.push([page_string,r,c])))
  get_image(...q.pop()).then(()=>{   // the last item should load completely first
    q.map(x=>get_image(...x))        // q should now be an array of promises
  }).catch(e=>console.log('failure in get_page',e))
  return Promise.all(q).catch(e=>console.log('failure in Promise.all',e))
}

var get_image = (page_string,row,col) => {
  var url = 'http://www.bl.uk/manuscripts/Proxy.ashx?view='+page_string+'_files/13/'+col+'_'+row+'.jpg'
  console.log(url)
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

var process_full_page = (page,rmax,cmax) => {
  exec('montage -geometry +0+0 -tile '+(cmax+1)+'x'+(rmax+1)+' '+page+'/* '+page+'.jpg',
    function (error, stdout, stderr) {
      console.log('stdout: ' + stdout)
      console.log('stderr: ' + stderr)
      if (error !== null) {console.log('exec error: ' + error)}
    }
  )
}

get_pages([3,4,5],3,3)

// console.log([2].map(page_string).forEach(page_string=>{
//   // get_page(page_string,12,16)
//   get_page(page_string,2,2)
// }))

// process_full_page('arundel_ms_263_f002v',2,2)

// process_full_page('arundel_ms_263_f001r',12,16)