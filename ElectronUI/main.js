const electron = require('electron');
const appEngine = electron.app;
const BrowserWindow = electron.BrowserWindow;

//console.log(electron);
let win;
function createWindow() {
  win = new BrowserWindow({width: 800, height: 600, webPreferences: {nodeIntegration: false}});
  win.loadURL(`file://${__dirname}/index.html`)

  win.webContents.openDevTools();
  win.on('closed', function(){
    win = null;
  });
}
const {PythonShell}  = require("python-shell")
PythonShell.run(
	"UIengine.py", null, function (err, results) {
        if (err) throw err
        console.log('UIengine.py finished')
        console.log('results', results)
    }
)

appEngine.on('ready', createWindow);

appEngine.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        appEngine.quit()
      }
});

appEngine.on('activate', () => {
  if (win === null) {
    createWindow();
  }
});