var THEMES = {
  'light':`
  --main-background-color:#fff;
  --font-color:#000;
  --link-color: #5252ff;
  --table-main:#999;
  --table-even:#b9b9b9;
  --table-odd: #ddd;`,
  'dark':`
  --main-background-color:#444;
  --font-color:#fff;
  --link-color: #568de6;
  --table-main:#111;
  --table-even:#222;
  --table-odd: #333;`
}

function loadTheme(theme) {
  let vars = THEMES[theme].split('\n');
  for (var i = 0; i < vars.length; i++) {
    let splits = vars[i].split(':');
    if(splits.length == 2){
      for(let i = 0;i<20;i++){
        splits[0] = splits[0].replace(' ','')
        splits[1] = splits[1].replace(' ','')
      }
      document.documentElement.style.setProperty(splits[0].replace(' ',''), splits[1].replace(';',''));
    }
  }
}
