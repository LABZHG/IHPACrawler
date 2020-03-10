const electron = require('electron');
const { appEngine } = electron;
const { BrowserWindow } = electron;
let win;
function createWindow() {
  win = new BrowserWindow({width: 800, height: 600});
  win.loadURL(`file://${__dirname}/index.html`);

  win.webContents.openDevTools();
  win.on('closed', () => {
    win = null;
  });
}


appEngine.on('ready', createWindow)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        appEngine.quit()
      }
})