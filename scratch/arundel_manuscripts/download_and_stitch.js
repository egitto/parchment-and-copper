var http = require('http');
var fs = require('fs');

var download = function(url, dest, cb) {
  var file = fs.createWriteStream(dest);
  var request = http.get(url, function(response) {
    response.pipe(file);
    file.on('finish', function() {
      file.close(cb);  // close() is async, call cb after close completes.
    });
  }).on('error', function(err) { // Handle errors
    fs.unlink(dest); // Delete the file async. (But we don't check the result)
    if (cb) cb(err.message);
  });
};

var page_string = (i) =>{
  var n = ''+(((i/2)|0)+1)
  console.log(n.length)
  n = '0'.repeat(3-n.length)+n
  return "arundel_ms_263_f"+n+(i%2?"v":"r")}

var get_image = (page_string,row,col) => {
  download('http://www.bl.uk/manuscripts/Proxy.ashx?view='+page_string+'_files/13/'+col+'_'+row+'.jpg',page_string+'_'+col+'_'+row+'.jpg',on_error)
}



console.log([0,1,2,10,20,500].map(page_string).forEach(page_string=>{

}))