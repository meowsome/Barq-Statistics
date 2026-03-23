import express from 'express';
const app = express();
import cors from 'cors';
import records from "./routes/record.js";

app.use(cors());
app.use(express.json());
app.use("/record", records);

app.listen(8080, () => {
      console.log('server listening on port 8080')
})

app.get('/', (req, res) => {
      res.send('Hello from our server!')
})