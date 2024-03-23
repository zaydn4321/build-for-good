const { ipcRenderer } = require('electron');

document.getElementById('goToSecondScreen').addEventListener('click', () => {
  ipcRenderer.send('change-window-content', './screens/second.html');
});
