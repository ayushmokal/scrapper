export const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const formatDate = () => {
  const date = new Date();
  return date.toISOString().split('T')[0];
};