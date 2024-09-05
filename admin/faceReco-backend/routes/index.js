import express from 'express';
import databaseRouter from './databaseRouter.js';
import userRouter from './userRouter.js';
import authRouter from './authRouter.js';

const router = express.Router();

router.use('/database', databaseRouter);
router.use('/users', userRouter);
router.use('/auth', authRouter);



export default router;
