import mongoose from 'mongoose';
import bcrypt from 'bcrypt';

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
  },
  phone: {
    type: String,
    required: true,
  },
  password: {
    type: String,
    required: true,
  },
  role: {
    type: String,
    enum: ['admin'], // Define possible roles
    default: 'admin',
  },
});

// Hash password before saving user to database
userSchema.pre('save', async function (next) {
  try {
    next();
  } catch (error) {
    next(error);
  }
});

// Method to compare passwords
userSchema.methods.comparePassword = async function (candidatePassword) {
  console.log(candidatePassword);
  return bcrypt.compare(candidatePassword, this.password);
};

export default mongoose.model('user', userSchema);
