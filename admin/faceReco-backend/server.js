import express from 'express';
import path from 'path';
const app = express();
import './config/connect-db.js';
import cors from 'cors';
import appService from "./services/app.js"
import routes from "./routes/index.js"
const __dirname = path.resolve();
app.use(
  cors({
    origin: '*',
  })
);
app.use(express.json({ limit: '50mb' }));
app.disable('x-powered-by');
const users = [
  {  email: 'nikunj.dhaduk7@gmail.com', password: '123456' },
];

// app.post('/login', (req, res) => {
//   const { email, password } = req.body;
//   if (!email || !password) {
//     return res
//       .status(400)
//       .json({ message: 'email and password are required' });
//   }
//   const user = users.find(
//     (u) => u.email === email && u.password === password
//   );
//   if (!user) {
//     return res.status(401).json({ message: 'Invalid email or password' });
//   }
//   res.status(200).json({ message: 'Login successful', user });
// });
// app.post('/flight-booking/add', async(req, res) => {
//     const body = req.body;
//     const bookFlight = await BookFlight.create(body);
//   res.status(200).json({ message: 'Flight Book successFully' });
// });
app.use(appService);
app.use('/', routes);

const port = 3001;
let serverInstance = app.listen(port, () => {
  console.log(`Listening at port ${port}`);
});
