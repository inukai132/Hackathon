'use strict';

// Enable app-relative includes (https://gist.github.com/branneman/8048520)
// Note: use require.main.require('file/path') for app-relative includes

const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const PORT = process.env.PORT || 8080;
const REALM = process.env.NODE_ENV || 'development';

// Initialize our Express class
const app = express();

// Enable Apache-like logging for all web requests
app.use(morgan('combined'));

// Redirect methods
if (REALM === 'production') {
	// Redirect all HTTP to HTTPS
	app.get('*', function(req, res, next) {
		if (req.headers['x-forwarded-proto'] != 'https') {
			res.redirect(BASE_URL + req.url);
		} else {
			next(); // Continue to other routes if we're not redirecting
		}
	});
}

// Tells server how to read incoming json or url data
app.use(bodyParser.urlencoded({
	extended: true,
}));

app.use(bodyParser.json());

// Specifies what folders have static files the server must read
app.use(express.static('images'));
app.use(express.static('scripts'));
app.use(express.static('css'));
app.use(express.static('html'));
app.use(express.static('routes'));
app.use(express.static('services'));
app.use(express.static('node_modules'));

// Tells the terminal the node has been created at a given port number
app.listen(PORT, function() {
	let url = '';

	if (REALM === 'development') {
		url = 'http://localhost:' + PORT + '/';
	} else {
		url = BASE_URL + '/';
	}

	console.log('[REALM ' + REALM + '] Portal now accepting requests at ' + url);
});
