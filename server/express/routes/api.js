import express from "express";
import db from "../db/connection.js";

const router = express.Router();

function arrayToLabelValues(results, labelTitle, valueTitle, type) {
    let valueKey; 
    let labelKey;
    switch (type) {
        case "pie":
            valueKey = "values"
            labelKey = "labels"
            break;

        case "bar":
            valueKey = "x"
            labelKey = "y"
            break;
    }

    const counts = {
        [valueKey]: [],
        [labelKey]: []
    };
    results.forEach(gender => {
        counts[labelKey].push(gender._id[labelTitle] ? gender._id[labelTitle] : "N/A");
        counts[valueKey].push(gender[valueTitle]);
    })

    return counts;
}

router.get("/coordinates", async (req, res) => {
    const collection = await db.collection(process.env.MONGODB_COLLECTION);

    // Get count of each occurance of coordinate from database
    const results = await collection.aggregate([
        {
$match: {
                "location.place.latitude": { $ne: null },
                "location.place.longitude": { $ne: null }
            }
        },
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
        { $limit: 6 }
    ]).toArray();

    const counts = arrayToLabelValues(results, 'genders', 'count', 'pie');

    res.send(counts).status(200);
});

router.get("/orientation", async (req, res) => {
    const collection = await db.collection(process.env.MONGODB_COLLECTION);

    const results = await collection.aggregate([
        {
            $group: {
                _id: {
                    sexualOrientation: "$bio.sexualOrientation",
                },
                count: { $sum: 1 }
            }
        },
        { $sort: { count: -1 } },
        { $limit: 9 }
    ]).toArray();

    const counts = arrayToLabelValues(results, 'sexualOrientation', 'count', 'pie');
    
    res.send(counts).status(200);
});

router.get("/relationship", async (req, res) => {
    const collection = await db.collection(process.env.MONGODB_COLLECTION);

    const results = await collection.aggregate([
        {
            $group: {
                _id: {
                    relationshipStatus: "$bio.relationshipStatus",
                },
                count: { $sum: 1 }
            }
        },
        { $sort: { count: -1 } },
        { $limit: 7 }
    ]).toArray();

    const counts = arrayToLabelValues(results, 'relationshipStatus', 'count', 'pie');

    res.send(counts).status(200);
});
    
    res.send(counts).status(200);
});


export default router;