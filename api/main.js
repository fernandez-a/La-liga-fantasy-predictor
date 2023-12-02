// main.js

const express = require('express');
const cron = require('node-cron');
const dotenv = require('dotenv');
const Data = require('./dataModel.js');
require('./db');


dotenv.config();


const app = express();
app.use(express.json());


app.get('/data', async (req, res) => {
    const data = await Data.find();
    res.json(data);
});

app.post('/data', async (req, res) => {
    const existingData = await Data.findOne({ Jornada: req.body.Jornada });

    if (existingData) {
        res.json({ message: 'Game week already added' });
    } else {
        const newData = new Data(req.body);
        await newData.save();
        res.json(newData);
    }
});


// cron.schedule('0 0 * * 0', async () => {
//     const stats = {}; // Fetch or calculate your stats here
//     const existingData = await Data.findOne({ Jornada: stats.Jornada });

//     if (!existingData) {
//         const newData = new Data(stats);
//         await newData.save();
//     }
// });


const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on port ${port}`));