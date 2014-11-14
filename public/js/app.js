$(function(){
  var setsRegex = /SETS\:([\s\S]*?)ENDSETS/i;
  $("#model_sets").keyup(function(){
    mySetsArray = this.value.split(/\s*;\s*/).slice(0, -1);
    if(mySetsArray.length > 0){
      var tables_obj = {}
      for(var i=0; i < mySetsArray.length; i++){
        content = mySetsArray[i].split(":");
        tables_obj[content[0]] = {
          columns: content[1]
        }
      }
      console.log(tables_obj)
    }else{
      console.log("NOTHIN TU SEE BOYS")
    }
  });
});
