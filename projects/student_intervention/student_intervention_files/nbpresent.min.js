/* global requirejs define */
define(
["require", "jquery", "base/js/namespace"],
function(require, $, Jupyter){
  // here's your namespace global
  var nbpresent = window.nbpresent = {loading: true};

  var initializedResolver,
    initializedPromise = new Promise(function(resolve, reject){
      initializedResolver = resolve;
    });

  var $dlMenu = $("#download_html").parent();

  var formats = [
    {key: "nbpresent", label: "Presentation (.html)"},
    {key: "nbpresent_pdf", label: "Presentation (.pdf)"}
  ];

  function load_ipython_extension() {
    initNbpresent();
  }

  function initialized(){
    return initializedPromise;
  }

  function initNbpresent(){
    requirejs.config({
      paths: {
        "nbpresent-deps": require.toUrl("./nbpresent.deps.min.js"),
        "nbpresent-notebook": require.toUrl("./nbpresent.notebook.min.js")
      }
    });

    var modulePath = requirejs.toUrl("nbpresent-notebook").split("?")[0]
      .split("/")
      .slice(0, -2)
      .join("/");

    initStylesheet(modulePath);


    requirejs(["nbpresent-deps"], function(){
      Jupyter.page.show_site();
      requirejs(["nbpresent-notebook"], function(mode){
        setTimeout(function(){
          nbpresent.mode = new mode.NotebookMode(
            require.toUrl(".").split("?")[0]
          );

          initializedResolver(nbpresent.mode);

          initToolbar();
          initMenu();
        }, 1000);
      });
    });
  }

  function show(){
    nbpresent.mode.show();
  }

  function present(){
    nbpresent.mode.present();
  }

  function nbconvert(key){
    Jupyter.menubar._nbconvert(key, true);
  }

  function initStylesheet(modulePath){
    var id = "nbp-css",
      $head = $("head"),
      cssPath = modulePath + "/css/nbpresent.min.css";

    $head.find("link#" + id).length || $("<link/>", {
      id: id,
      rel: "stylesheet",
      href: cssPath,
    }).appendTo($head);
  }

  // set up the UI before doing anything else to avoid UI delay
  function initToolbar(){
    $("#view_menu").append(
      $("<li/>").append(
        $("<a/>").text("Toggle Presentation").on("click", show)));

    // TODO: make this one button!
    Jupyter.toolbar.add_buttons_group([
      {
        label: "Edit Presentation",
        icon: "fa-gift",
        callback: show,
        id: "nbp-app-btn"
      },
      {
        label: "Show Presentation",
        icon: "fa-youtube-play",
        callback: present,
        id: "nbp-present-btn"
      }
    ]);
  }

  function initMenu(){
    $.get(Jupyter.notebook.base_url + "api/nbconvert", formatsLoaded);
  }

  function dlMenuItem(format){
    $("<li/>")
      .append(
        $("<a/>", {"class": "download_" + format.key})
          .text(format.label)
          .on("click", function(){ nbconvert(format.key); })
      )
      .appendTo($dlMenu)
  }

  function formatsLoaded(available){
    // update the download chrome
    formats.map(function(format){
      available[format.key] && dlMenuItem(format);
    });
  }

  return {
    load_ipython_extension: load_ipython_extension,
    initialized: initialized
  };
});
