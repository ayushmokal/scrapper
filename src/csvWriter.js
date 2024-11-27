import { createObjectCsvWriter } from 'csv-writer';
import { formatDate } from './utils.js';

export async function saveToCsv(doctors, zipCode) {
  const date = formatDate();
  const filename = `doctors_${zipCode}_${date}.csv`;
  
  const csvWriter = createObjectCsvWriter({
    path: filename,
    header: [
      { id: 'name', title: 'Name' },
      { id: 'address', title: 'Address' },
      { id: 'phone', title: 'Phone Number' }
    ]
  });

  await csvWriter.writeRecords(doctors);
  return filename;
}