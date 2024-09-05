import catchAsync from '../untils/catchAsync.js';
import User from '../modal/user.js';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

const authController = {
  // Book room API endpoint
  register: catchAsync(async (req, res) => {
    const { username, email, password, phone } = req.body;

    // try {
      const user = new User({ username, email, password, phone });

      user.role = 'admin';

      await user.save();

      res
        .status(201)
        .json({ message: 'User registered successfully as admin' });
    // } catch (error) {
    //   res.status(500).json({ error: 'Failed to register user' });
    // }
  }),
  login: catchAsync(async (req, res) => {
    const { email, password } = req.body;
    console.log('req.body', req.body)
    //   try {
    // Check if user exists
    let user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ error: 'User not found' });
    }
    
    // Compare passwords
    const isMatch = await bcrypt.compare(password, user.password);
    console.log(isMatch, password, user.password);
    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // If credentials are valid, generate JWT token
    const tokenPayload = {
      userId: user._id,
      userName: user.userName,
      email: user.email,
    };
    const token = jwt.sign(tokenPayload, 'hotel', {
      expiresIn: '1h',
    });
    console.log('user', user);

    // Send response with user information and token
    res.json({
      userName: user.username ,
      email: user.email,
      role: user?.role,
      phone: user?.phone,
      token,
    });
    //   } catch (error) {
    //     console.error(error);
    //     res.status(500).json({ error: 'Server error' });
    //   }
  }),
};
export default authController;
