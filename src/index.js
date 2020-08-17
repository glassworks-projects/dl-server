import 'dotenv/config';
import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());

app.listen(process.env.PORT, () => {
	console.log(`app listening on port ${process.env.PORT}!`);	
});
console.log(`pw: ${process.env.MY_SECRET}`);
console.log("check me ouuuuuut!");
