// Import necessary modules
import express from 'express';
import userController from '../controller/userController.js';


// Create a router instance
const router = express.Router();

// Define routes
router.post('/add', userController.add);
router.put('/update/:id', userController.update);
router.get('/single/:id', userController.single);
router.delete('/delete/:id', userController.delete);
router.get('', userController.list);

// Export the router
export default router;
