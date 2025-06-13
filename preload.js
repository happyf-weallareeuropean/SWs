const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('xcap', {
  requestCapture: () => ipcRenderer.send('capture-request'),
  onCaptureResponse: (callback) => ipcRenderer.on('capture-response', (_e, data) => callback(data)),
});
