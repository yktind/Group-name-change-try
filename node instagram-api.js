const { IgApiClient } = require('instagram-private-api');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

let ig;

// Login route
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        ig = new IgApiClient();
        ig.state.generateDevice(username);

        await ig.account.login(username, password);
        res.status(200).json({ message: 'Login successful' });
    } catch (error) {
        res.status(400).json({ error: 'Login failed', details: error.message });
    }
});

// Send messages
app.post('/send-message', async (req, res) => {
    const { groupId, messages, delay } = req.body;

    if (!ig) {
        return res.status(400).json({ error: 'Please login first' });
    }

    try {
        for (let i = 0; i < messages.length; i++) {
            await ig.entity.directThread([groupId]).broadcastText(messages[i]);

            console.log(`Sent message ${i + 1}: ${messages[i]}`);
            await new Promise(resolve => setTimeout(resolve, delay * 1000));
        }

        res.status(200).json({ message: 'Messages sent successfully' });
    } catch (error) {
        res.status(500).json({ error: 'Failed to send messages', details: error.message });
    }
});

app.listen(3000, () => {
    console.log('Instagram API server running on port 3000');
});
