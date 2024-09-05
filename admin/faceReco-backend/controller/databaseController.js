import catchAsync from '../untils/catchAsync.js';
import Database from '../modal/database.js';

const databaseController = {
  add: catchAsync(async (req, res) => {
    try {
      const { name, email, organizations,  city, pinCode, country, state } =
        req.body;
      const existingUser = await Database.findOne({ email });
      if (existingUser) {
        return res
          .status(400)
          .json({ error: 'Database with this email already exists' });
      }

      const database = new Database({
        name,
        email,
        organizations,
        city,
        pinCode,
        country,
        state,
      });
      await database.save();
      res.status(201).json(database);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }),
  update: catchAsync(async (req, res) => {
    try {
      const {
        name,
        email,
        organizations,
        
        city,
        pinCode,
        country,
        state,
        suspect,
      } = req.body;
      const database = await Database.findByIdAndUpdate(
        req.params.id,
        {
          name,
          email,
          organizations,
          city,
          pinCode,
          country,
          state,
          suspect,
        },
        { new: true }
      );
      if (!database) {
        return res.status(404).json({ error: 'Database not found' });
      }
      res.json(database);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }),
  single: catchAsync(async (req, res) => {
    try {
      const { id } = req.params;
      const {
        name,
        email,
        organizations,
        
        city,
        pinCode,
        country,
        state,
        suspect,
      } = req.body;

      // Check if ID is provided in the request
      if (id) {
        const database = await Database.findByIdAndUpdate(
          id,
          {
            name,
            email,
            organizations,
            
            city,
            pinCode,
            country,
            state,
            suspect,
          },
          { new: true }
        );
        if (!database) {
          return res.status(404).json({ error: 'Database not found' });
        }
        return res.json(database);
      } else {
        const existingUser = await Database.findOne({ email });
        if (existingUser) {
          return res
            .status(400)
            .json({ error: 'Database with this email already exists' });
        }
        const newUser = new Database({
          name,
          email,
          organizations,
          
          city,
          pinCode,
          country,
          state,
          suspect,
        });
        await newUser.save();
        return res.status(201).json(newUser);
      }
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }),
  delete: catchAsync(async (req, res) => {
    try {
      const { id } = req.params;
      const database = await Database.findByIdAndDelete(id);
      if (!database) {
        return res.status(404).json({ error: 'Database not found' });
      }
      return res.json({ message: 'Database deleted successfully' });
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }),
  list: catchAsync(async (req, res) => {
    try {
      const database = await Database.find();
      return res.json(database);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }),
};
export default databaseController;
