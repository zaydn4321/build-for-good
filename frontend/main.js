const { app, BrowserWindow, ipcMain } = require('electron');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false, // Remember, for production it's better to use context isolation
    }
  });

  mainWindow.loadFile('./screens/first.html');
}

app.whenReady().then(createWindow);

ipcMain.on('navigate-to-second', () => {
  mainWindow.loadFile('./screens/second.html');
});

ipcMain.on('navigate-to-first', () => {
  mainWindow.loadFile('./screens/first.html');
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
