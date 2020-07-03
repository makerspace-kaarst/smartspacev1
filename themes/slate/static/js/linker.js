var links = document.links;
for (var i = 0, linksLength = links.length; i < linksLength; i++) {
  if (links[i].hostname != window.location.hostname) {
    links[i].target = '_blank';
    links[i].innerHTML = links[i].innerHTML.replace("class=","target='_blank' class=")
  }
}
