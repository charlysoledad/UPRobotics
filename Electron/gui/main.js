const electron = require("electron");
const app= electron.app;
const path = require('path');
const BrowserWindow = electron.BrowserWindow;
const main_width=800;
const main_height=600;

var openWindow=(filename,_width,_height,_minWidth=_width,_minHeight=_height,_transparent=false,_frame=true,_aot=false,_debug=false,_max=false)=>{
    let win=new BrowserWindow({width:_width, height:_height,minWidth:_minWidth, minHeight:_minHeight,transparent:_transparent,frame:_frame,alwaysOnTop:_aot,});
    if(_max)win.maximize();
    if(_debug)win.webContents.openDevTools();
    win.loadURL(`file://${__dirname}/`+filename+`.html`);
    //win.setIcon(path.join(__dirname, `vistas/assets/img/cons-icons/16x16.png`));
}

app.on("ready",()=>{
    console.log("app started")
    openWindow("index",1200,680,300,500,false,true,false,false,true);
    //openWindow("vistas/menu_debug",500,500,300,300,true,false,false,false,true);
    //openWindow("vistas/nuevo_reporte",500,500,300,300,true,false,false,false,true);
});

app.on("window-all-closed",()=>{
    app.quit()
});

module.exports={openWindow};