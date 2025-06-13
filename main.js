const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const screenshots = require('node-screenshots');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.on('capture-request', async (event) => {
  try {
    const image = await screenshots.captureScreenshot();
    // Here we would process the screenshot if needed
    event.reply('capture-response', { success: true });
  } catch (err) {
    event.reply('capture-response', { success: false, error: err.message });
  }
});
