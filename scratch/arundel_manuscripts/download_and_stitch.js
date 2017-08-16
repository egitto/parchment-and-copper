var http = require('http');
var fs = require('fs');
var exec = require('child_process').exec, child
var _ = require('underscore')

var download = function(url, dest, cb) {
  in_progress_downloads ++
  var file = fs.createWriteStream(dest);
  var request = http.get(url, function(response) {
    response.pipe(file);
    file.on('finish', function() {
      file.close(cb(dest)).then(return Promise(resolve(dest)));  // close() is async, call cb after close completes.
    }).then(return Promise.resolve(dest));
  }).on('error', function(err) { // Handle errors
    in_progress_downloads --
    fs.unlink(dest); // Delete the file async. (But we don't check the result)
    console.log(err,url,dest)
  }).then(console.log('error?'));
};

var pad_int = (n,pad) => {
    return '0'.repeat((pad?pad:3)-(''+n).length)+n
}

var page_string = (i) =>{
  var n = pad_int(((i/2)|0)+1)
  console.log(n.length)
  return "arundel_ms_263_f"+n+(i%2?"v":"r")}

var get_pages = (pages,rows,cols) => {

}

var get_page = (page_string,rows,cols) => {
  if (!fs.existsSync(page_string)){
    fs.mkdirSync(page_string);
  }
  var q = []
  _.range(rows).forEach(r=>_.range(cols).forEach(c=>q.push([page_string,r,c])))
  while(q.length > 0){
    get_image(...q.pop())
  }
}

var get_image = (page_string,row,col) => {
  var url = 'http://www.bl.uk/manuscripts/Proxy.ashx?view='+page_string+'_files/13/'+col+'_'+row+'.jpg'
  console.log(url)
  var path = page_string+'/'+page_string.match(/f\d\d\d\w/)[0]+'_r'+pad_int(row)+'_c'+pad_int(col)+'.jpg'
  download(url,path,process_downloaded)
}

var files_struct = {}
var in_progress_downloads = 0
var process_downloaded = (dest) => {
  in_progress_downloads --
  var page = dest.match(/arundel_ms_263_f\d\d\d\w/)[0]
  var r = parseInt(dest.match(/r\d+/).slice(1))
  var c = parseInt(dest.match(/c\d+/).slice(1))
  if(!files_struct[page]){files_struct[page]={id: page, rmax: 0, cmax: 0, items: []}}
  if(fs.readFileSync(dest).toString('utf8').slice(0,5)==='http:'){fs.unlink(dest); return false} // 404 error
  var entry = files_struct[page]
  entry.rmax = _.max([r,entry.rmax])
  entry.cmax = _.max([c,entry.cmax])
  console.log(entry.items.push(dest),(entry.rmax+1)*(entry.cmax+1))
  if(entry.items.length === (entry.rmax+1)*(entry.cmax+1)){
    process_full_page(page,entry.rmax,entry.cmax); console.log(page,'finished'); return true
  }
  return false
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

console.log([2].map(page_string).forEach(page_string=>{
  // get_page(page_string,12,16)
  get_page(page_string,2,2)
}))

// process_full_page('arundel_ms_263_f001r',12,16)