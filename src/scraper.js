import { createBrowser, closeBrowser } from './browser.js';
import { sleep } from './utils.js';

async function getDoctorUrls(page, zipCode) {
  const url = `https://health.usnews.com/doctors/search?distance=250&location=${zipCode}&np_pa=false&specialty=Urology&sort=distance`;
  await page.goto(url, { waitUntil: 'networkidle0' });
  await sleep(2000);
  
  const doctorUrls = await page.evaluate(() => {
    const links = document.querySelectorAll('a[href*="/doctors/"]');
    return Array.from(links)
      .map(link => link.href)
      .filter(href => href.match(/\/doctors\/[\w-]+-\d+$/));
  });
  
  return [...new Set(doctorUrls)];
}

async function getDoctorDetails(page, url) {
  await page.goto(url, { waitUntil: 'networkidle0' });
  await sleep(1000);
  
  return await page.evaluate(() => {
    const name = document.querySelector('h1')?.textContent?.trim() || 'N/A';
    const addressElement = document.querySelector('p.fBaaRL');
    const phoneElement = document.querySelector('a[href^="tel:"]');
    
    return {
      name,
      address: addressElement?.textContent?.trim() || 'N/A',
      phone: phoneElement?.textContent?.trim() || 'N/A',
      profileUrl: window.location.href
    };
  });
}

export async function scrapeUrologistData(zipCode) {
  let browser, chrome;
  const uniqueDoctors = new Map();
  const doctorDetails = [];

  try {
    ({ browser, chrome } = await createBrowser());
    const page = await browser.newPage();
    await page.setDefaultTimeout(30000);
    
    const urls = await getDoctorUrls(page, zipCode);
    console.log(`Found ${urls.length} doctor profiles`);
    
    for (const url of urls) {
      const doctorInfo = await getDoctorDetails(page, url);
      const doctorKey = `${doctorInfo.name.toLowerCase()}-${doctorInfo.address.toLowerCase()}`;
      
      if (!uniqueDoctors.has(doctorKey)) {
        uniqueDoctors.set(doctorKey, doctorInfo);
        doctorDetails.push(doctorInfo);
        console.log(`Found doctor: ${doctorInfo.name}`);
      }
    }
    
    return Array.from(uniqueDoctors.values());
  } catch (error) {
    console.error('Scraping error:', error.message);
    throw error;
  } finally {
    await closeBrowser(browser, chrome);
  }
}