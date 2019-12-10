function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

while (true){
  console.log("Hi");
  await sleep(5000);
}