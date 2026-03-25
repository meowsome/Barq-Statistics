import express from 'express';
const app = express();
import cors from 'cors';
import api from "./routes/api.js";

app.use(cors());
app.use(express.json());
app.use("/api", api);

app.listen(8080, () => {
      console.log('server listening on port 8080')
})

app.get('/', (req, res) => {
      res.send('Hello from our server!')
})