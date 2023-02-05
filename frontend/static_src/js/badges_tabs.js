String.prototype.trimLeft = function(charlist) {
  if (charlist === undefined)
    charlist = "\s";

  return this.replace(new RegExp("^[" + charlist + "]+"), "");
};

function showTab(tabId) {
    // Remove "is-active" from all tabs but tabId and add it to the correct one
    document.querySelectorAll(`li.tab.is-active:not(#${tabId}-tab)`)
        .forEach(function (tab) {
        tab.classList.remove("is-active");
    });
    document.querySelector(`li.tab#${tabId}-tab`).classList.add("is-active");

    // Toggle the info panel\
    document.querySelectorAll(`.badges-info.is-active:not(#${tabId}-info)`)
        .forEach(function (panel) {
        panel.classList.remove("is-active");
    })
    document.querySelector(`.badges-info#${tabId}-info`).classList.add("is-active");
}

document.addEventListener("DOMContentLoaded", function(event) {
    if (window.location.hash) {
        showTab(window.location.hash.trimLeft("#"));
    }

    // Get all of the tabs
    let tabs = document.querySelectorAll("li.tab a");
    tabs.forEach(function(tab) {
        tab.addEventListener("click", function () {
            showTab(this.dataset.target);
        })
    });
});