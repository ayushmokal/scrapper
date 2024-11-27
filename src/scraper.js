import { createBrowser, closeBrowser } from './browser.js';
import { sleep } from './utils.js';

export async function scrapeUrologistData(zipCode) {
  let browser, chrome;

  try {
    ({ browser, chrome } = await createBrowser());
    const page = await browser.newPage();
    
    // Set a reasonable timeout
    await page.setDefaultTimeout(30000);

    const url = `https://health.usnews.com/doctors/search?distance=250&location=${zipCode}&np_pa=false&specialty=Urology&sort=distance`;
    await page.goto(url, { waitUntil: 'networkidle0' });
    
    // Wait for initial load and handle potential cookie consent
    await sleep(2000);
    
    // Scroll to load more results if available
    await autoScroll(page);

    const doctors = await page.evaluate(() => {
      const doctorElements = document.querySelectorAll('.search-result');
      return Array.from(doctorElements).map(element => {
        const nameElement = element.querySelector('.search-result__name');
        const addressElement = element.querySelector('.search-result__address');
        const phoneElement = element.querySelector('.search-result__phone');

        return {
          name: nameElement ? nameElement.textContent.trim() : 'N/A',
          address: addressElement ? addressElement.textContent.trim() : 'N/A',
          phone: phoneElement ? phoneElement.textContent.trim() : 'N/A'
        };
      });
    });

    return doctors;
  } catch (error) {
    console.error('Scraping error:', error.message);
    throw error;
  } finally {
    await closeBrowser(browser, chrome);
  }
}

async function autoScroll(page) {
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let totalHeight = 0;
      const distance = 100;
      const timer = setInterval(() => {
        const scrollHeight = document.documentElement.scrollHeight;
        window.scrollBy(0, distance);
        totalHeight += distance;

        if (totalHeight >= scrollHeight) {
          clearInterval(timer);
          resolve();
        }
      }, 100);
    });
  });
  
  // Wait for any dynamic content to load
  await sleep(1000);
}