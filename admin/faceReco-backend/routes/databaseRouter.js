// Import necessary modules
import express from 'express';
import databaseController from '../controller/databaseController.js';

// Create a router instance
const router = express.Router();

// Define routes
router.post('/add', databaseController.add);
router.put('/update/:id', databaseController.update);
router.get('/single/:id', databaseController.single);
router.delete('/delete/:id', databaseController.delete);
router.get('', databaseController.list);

// Export the router
export default router;
