import express from "express";
import db from "../db/connection.js";

const router = express.Router();

router.get("/", async (req, res) => {
    const collection = await db.collection(process.env.MONGODB_COLLECTION);

    // Get count of each occurance of coordinate from database
    const results = await collection.aggregate([
        {
            $group: {
                _id: {
                    latitude: "$location.place.latitude",
                    longitude: "$location.place.longitude"
                },
                count: { $sum: 1 }
            }
        }
    ]).toArray();
    

    // Turn into array of arrays instead of array of objects, turning count into percentage for intensity
    const max = Math.max(...results.map(coord => coord.count));
    const counts = results.map(result => ([result._id.latitude, result._id.longitude, result.count / max]));

    res.send(counts).status(200);
});

export default router;