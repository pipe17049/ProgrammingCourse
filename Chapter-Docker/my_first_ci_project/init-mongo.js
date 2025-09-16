// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

print('Starting MongoDB initialization...');

// Switch to the application database
db = db.getSiblingDB('my_first_ci_db');

// Create a user for the application (if needed)
// db.createUser({
//   user: 'app_user',
//   pwd: 'app_password',
//   roles: [{
//     role: 'readWrite',
//     db: 'my_first_ci_db'
//   }]
// });

// Create any initial collections or data if needed
db.createCollection('test_collection');

print('MongoDB initialization completed.'); 