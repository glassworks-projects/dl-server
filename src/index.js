import 'dotenv/config';
import express from 'express';
import { PythonShell } from 'python-shell';

const NOT_FOUND = 'not found';
const USED = 'used';
const VALID = 'valid';

const bodyParser = require('body-parser');
const app = express();

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

		pyshell.on('message', function (message) {
			// received a message sent from the Python script (a simple "print" statement)
			switch(message) {
				case NOT_FOUND: {
					res.sendStatus(404);
					break;
				}

				case USED: {
					res.status(403).send('Code already used');
					break;
				}

				case VALID: {
					res.sendFile(process.env.ASSET_PATH);
					break;
				}

				default: {
					res.status(500).send(
						'Encountered an unexpected response when validating download code'
					);
					break;
				}
			};
		});
		
		// end the input stream and allow the process to exit
		pyshell.end(function (err) {
			if (err) throw err;
		});
	} else {
		res.status(400).send("No download code provided");
	}
})