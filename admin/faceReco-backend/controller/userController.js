import catchAsync from '../untils/catchAsync.js';
import User from "../modal/user.js"
import bcrypt from 'bcrypt';

const userController = {
  add: catchAsync(async (req, res) => {
    try {
      const { username, email, password,phone, role } = req.body;
      const existingUser = await User.findOne({ email });
      if (existingUser) {
        return res
          .status(400)
          .json({ error: 'User with this email already exists' });
      }
      const hashedPassword = await bcrypt.hash(password, 10);
      const user = new User({
        username,
        email,
        password: hashedPassword,
        phone,
        role,
      });
      await user.save();
      res.status(201).json(user);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }),
  update: catchAsync(async (req, res) => {
     try {
       const { username, email, password,  phone } = req.body;
        const hashedPassword = await bcrypt.hash(password, 10);
       const database = await User.findByIdAndUpdate(
         req.params.id,
         {
           username,
           email,
           password: hashedPassword,
           phone,
           phone
         },
         { new: true }
       );
       if (!database) {
         return res.status(404).json({ error: 'User not found' });
       }
       res.json(database);
     } catch (error) {
       res.status(500).json({ error: error.message });
     }
  }),
  single: catchAsync(async (req, res) => {
    try {
      const user = await User.findById(req.params.id);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      res.json(user);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }),
  delete: catchAsync(async (req, res) => {
    try {
      const user = await User.findByIdAndDelete(req.params.id);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      res.json({ message: 'User deleted successfully' });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }),
  list: catchAsync(async (req, res) => {
try {
  const users = await User.find();
  res.json(users);
} catch (error) {
  res.status(500).json({ error: error.message });
}
  })
};
export default userController;
