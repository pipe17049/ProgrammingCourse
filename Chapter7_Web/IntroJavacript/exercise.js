const devs = [
  {
    name: "Eduardo",
    lastName: "Arias",
    age: 28,
    contactInfo: {
      phone: 3000000,
      email: "julianeduardoarias@outlook.com",
    },
    experience: {
      languages: ["Python", "Scala", "Clojure", "Java"],
    },
  },
];

const createContactInfo = (phone, email) => {};
const createExperience = (languages, tecnologies) => {};

function createDev(name, lastName, age, phone, email, languages, tecnologies) {
  // More code here
  return {
    name,
    lastName,
    age,
    contactInfo,
    // and here
  };
}

//devs.push(createDev())

function getDevByNameAndEmail(devName, devEmail) {
  const results = [];
  for (const dev of devs) {
    const { name, contactInfo } = dev;
    if (devName == name && devEmail == contactInfo.email) {
      results.push(dev);
    }
  }
  return results;
}

const devFound = getDevByNameAndEmail(
  "Eduardo",
  "julianeduardoarias@outlook.com"
);

console.log(devFound);
