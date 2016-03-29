var cmdFmt = 'node main.js <input-file> <output-file> <index-name> <type-name>';
var example = 'node main.js mongo.json es.json prod fairs';
if (process.argv.length !== 6) {
  console.log('Bad format, convert cancelled.');
  console.log('Format:');
  console.log(cmdFmt);
  console.log('Example:');
  console.log(example);
  return;
}

fs = require('fs');
var fairs = require('./' + process.argv[2]);

var esfs = fairs.map(function(elem, index) {
  var esf = {
    '_index': process.argv[4],
    '_type': process.argv[5],
    '_id': elem._id,
    '_score': 0
  };
  delete elem._id;
  esf['_source'] = elem;
  return esf;
});

var targetFile = process.argv[3];
try {
  fs.truncateSync(targetFile, 0);
} catch (err) {
  if (err.code !== 'ENOENT') {  // log when the error is not "file not found"
    console.log(err.code);
  }
}

esfs.forEach(function(elem) {
  fs.appendFileSync(targetFile, JSON.stringify(elem));
});
