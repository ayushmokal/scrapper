import { scrapeUrologistData } from './scraper.js';
import { saveToCsv } from './csvWriter.js';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const zipCode = process.argv[2] || process.env.DEFAULT_ZIP_CODE || '10081';
  
  try {
    console.log(`Starting scraping for zip code: ${zipCode}`);
    console.log('This may take a few moments...');
    
    const doctors = await scrapeUrologistData(zipCode);
    
    if (doctors.length === 0) {
      console.log('No doctors found for the specified location.');
      process.exit(0);
    }
    
    const filename = await saveToCsv(doctors, zipCode);
    console.log(`✓ Scraping completed successfully`);
    console.log(`✓ Found ${doctors.length} doctors`);
    console.log(`✓ Data saved to ${filename}`);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();