// data.js
const generateDummyData = (count) => {
  const names = [
    "Aarav", "Aarna", "Aarush", "Aayushi", "Advait", "Aisha", "Ananya", "Aarohi", "Amit", "Akshay",
    "Bhavya", "Bhavesh", "Chirag", "Chitra", "Dhruv", "Divya", "Gaurav", "Gitanjali", "Hari", "Ishaan",
    "Jasmine", "Jatin", "Kavya", "Kunal", "Leela", "Mohan", "Manisha", "Neha", "Naveen", "Ojas",
    "Pooja", "Pranav", "Rahul", "Riya", "Sachin", "Sanya", "Tarun", "Trisha", "Uday", "Vandana",
    "Vikram", "Yash", "Yamini", "Zoya"
  ];
  const products = [
    "Product A", "Product B", "Product C", "Product D", "Product E", "Product F", "Product G", "Product H", "Product I", "Product J"
  ];
  const distributions = ["India", "USA", "Canada", "UK"];
  const statuses = ["Active", "Inactive"];

  const data = [];
  for (let i = 1; i <= count; i++) {
    const name = names[Math.floor(Math.random() * names.length)];
    const product = products[Math.floor(Math.random() * products.length)];
    const distribution = distributions[Math.floor(Math.random() * distributions.length)];
    const status = statuses[Math.floor(Math.random() * statuses.length)];
    const price = Math.floor(Math.random() * 1000) + 100; // Generate a random price between 100 and 1099
    const date = getRandomDate(new Date(2020, 0, 1), new Date()); // Generate a random date

    data.push({ 
      refId: i,
      name,
      product,
      date,
      distribution,
      status,
      price
    });
  }
  return data;
};

// Function to generate a random date between two dates
const getRandomDate = (start, end) => {
  return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
};

export default generateDummyData;
