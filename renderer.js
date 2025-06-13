const button = document.getElementById('target-button');
let clickCount = 0;
let clickTimer;
const CLICK_THRESHOLD = 5; // Number of clicks
const TIME_WINDOW = 2000; // 2 seconds

function resetClicks() {
  clickCount = 0;
  clearTimeout(clickTimer);
}

button.addEventListener('click', () => {
  if (clickCount === 0) {
    clickTimer = setTimeout(resetClicks, TIME_WINDOW);
  }
  clickCount++;

  if (clickCount >= CLICK_THRESHOLD) {
    resetClicks();
    // Request a capture using xcap when repeated clicks detected
    window.xcap.requestCapture();
  }
});

window.xcap.onCaptureResponse((data) => {
  if (data.success) {
    console.log('Capture completed');
  } else {
    console.error('Capture failed', data.error);
  }
});
