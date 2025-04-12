const tables = document.querySelectorAll(
  "a[_ngcontent-ccw-c41][target][data-tooltip]"
);

const hrefList = Array.from(tables).map((a) => a.href);

console.log(hrefList);
