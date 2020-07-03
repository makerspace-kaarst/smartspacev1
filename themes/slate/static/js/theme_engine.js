var THEMES = {
  'l':`
  --main-background-color:#fff;
  --font-color:#000;
  --link-color: #5252ff;
  --table-main:#999;
  --table-even:#b9b9b9;
  --table-odd: #ddd;`,
  'd':`
  --main-background-color:#444;
  --font-color:#fff;
  --link-color: #568de6;
  --table-main:#111;
  --table-even:#222;
  --table-odd: #333;`
};

var NEXTTHEME = {
  'd':'l',
  'l':'d'
};

function loadTheme(theme) {
  let vars = THEMES[theme].split('\n');
  for (var i = 0; i < vars.length; i++) {
    let splits = vars[i].split(':');
    if(splits.length == 2){
      for(let i = 0;i<20;i++){
        splits[0] = splits[0].replace(' ','');
        splits[1] = splits[1].replace(' ','');
      }
      document.documentElement.style.setProperty(splits[0].replace(' ',''), splits[1].replace(';',''));
    }
  }
}


function setCookie(cname, cvalue) {
  a = new Date((new Date()).getTime() + 1000 * 60 * 60 * 24 * 365);
  document.cookie = cname + "=" + cvalue + ";expires=" + a.toGMTString() + ';';
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function loadFromCookie() {
  global_theme = getCookie('theme');
  loadTheme(global_theme);
}

function toggleTheme() {
  let th = getCookie('theme');
  setCookie('theme',NEXTTHEME[th]);
  loadFromCookie();
}


try {
  loadFromCookie();
} catch (e) {
  let th = {'#000':'d','#fff':'l'}[getComputedStyle(document.body).getPropertyValue('--color-scheme')]
  setCookie('theme',th);
  loadFromCookie();
} finally {

}
