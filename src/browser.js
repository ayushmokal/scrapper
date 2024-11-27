import puppeteer from 'puppeteer-core';
import chromeLauncher from 'chrome-launcher';

export async function createBrowser() {
  const chrome = await chromeLauncher.launch({
    chromeFlags: ['--headless', '--no-sandbox']
  });

  const browser = await puppeteer.connect({
    browserURL: `http://localhost:${chrome.port}`,
    defaultViewport: { width: 1920, height: 1080 }
  });

  return { browser, chrome };
}

export async function closeBrowser(browser, chrome) {
  if (browser) {
    await browser.close();
  }
  if (chrome) {
    await chrome.kill();
  }
}