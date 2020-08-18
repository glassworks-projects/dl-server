import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { PythonShell } from 'python-shell';

const NOT_FOUND = 'not found';
const USED = 'used';
const VALID = 'valid';

const app = express();
const bodyParser = require('body-parser');

app.use(cors());
app.use(bodyParser.urlencoded({
    extended: true
}));

app.use(express.json());

const options = {
	mode: 'text',
	pythonOptions: ['-u'], // get print results in real-time
	scriptPath: process.env.SCRIPT_PATH
  };

app.listen(process.env.PORT, () => {
	console.log(`app listening on port ${process.env.PORT}!`);	
});

app.post("/python-test", (req, res) => {
	
	const code = req.body?.code || undefined;
	
	if (code) {
		options.args = [code]
		const pyshell = new PythonShell('codes.py', options);
		let data;

		pyshell.on('message', function (message) {
			// received a message sent from the Python script (a simple "print" statement)
			switch(message) {
				case NOT_FOUND: {

					break;
				}

				case USED: {

					break;
				}

				case VALID: {

					break;
				}

				default: break;
			};
		});
		
		// end the input stream and allow the process to exit
		pyshell.end(function (err) {
			if (err) throw err;
			res.send(data);
		});
	}; // otherwise do something else
})