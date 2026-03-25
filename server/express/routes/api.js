import express from "express";
import db from "../db/connection.js";

const router = express.Router();

router.get("/coordinates", async (req, res) => {
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

router.get("/count", async (req, res) => {
    const collection = await db.collection(process.env.MONGODB_COLLECTION);

    const result = await collection.countDocuments();

    res.send(result).status(200);
});

router.get("/genders", async (req, res) => {
    const collection = await db.collection(process.env.MONGODB_COLLECTION);

    const results = await collection.aggregate([
        { $unwind: "$bio.genders" },
        {
            $group: {
                _id: {
                    genders: "$bio.genders",
                },
                count: { $sum: 1 }
            }
        },
        { $sort: { count: -1 } },
        { $limit: 5 }
    ]).toArray();

    const counts = {
        "labels": results.map(result => result._id.genders),
        "counts": results.map(result => result.count)
    }
    
    res.send(counts).status(200);
});


export default router;