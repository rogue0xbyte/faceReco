import mongoose from 'mongoose';
import { readFileSync } from 'fs';

mongoose.Promise = global.Promise;
console.log('process.env.MONGO_URL', process.env.MONGO_URL);
(async function () {
  try {
    const configFile = '../../config.json'
    const config = JSON.parse(readFileSync(configFile, 'utf8'));
    const mongooseURL = config.mongo;
    await mongoose.connect(mongooseURL, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('DB connection successfully');
  } catch (error) {
    console.log('Could not connect to the database. Exiting now...', error);
    process.exit();
  }
})();
