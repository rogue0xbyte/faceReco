// Import necessary modules
import express from 'express';
import authController from '../controller/authController.js'


// Create a router instance
const router = express.Router();

// Define routes
router.post('/register', authController.register);
router.post('/login', authController.login);

// Export the router
export default router;
