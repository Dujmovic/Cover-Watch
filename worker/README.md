# Cover Watch lock-screen alerts (Cloudflare Worker)

`worker.js` is the whole helper. It is built from `worker.src.js` plus the bet logic in `../index.html` by `python3 build.py`, so the alert wording and the cover math always match the app. Do not edit `worker.js` by hand.

What it does: once a minute it checks ESPN for the games in everyone's open bets, works out whether any bet changed status or a team scored, and sends a Web Push message to that person's phone. Nothing is sent to a phone while its app is open on screen.

One helper can serve several people (up to 15). Each phone gets its own random ID from the app, so bets, alerts and settings stay separate. ESPN is asked once per game no matter how many people follow it.

## Setup (about 15 minutes, on a computer)

You need a free Cloudflare account, and the iPhone on iOS 16.4 or newer with Cover Watch opened from its Home Screen icon.

1. Cloudflare dashboard, **Workers & Pages**, **Create**, start with **Hello World**, name it `coverwatch`, **Deploy**.
2. **Edit code**. Select everything, delete it, and paste the contents of `worker.js`. **Deploy**.
3. **Storage & Databases**, **KV**, **Create** a namespace named `coverwatch`.
4. Back in the Worker: **Settings**, **Bindings**, **Add**, **KV namespace**. Variable name `KV` (capital letters), choose the `coverwatch` namespace, save.
5. **Settings**, **Variables and Secrets**, **Add**. Type **Secret**, name `TOKEN`, value is an access code you invent (16 or more characters). To serve friends, give each person their own code and enter them all separated by commas, like `code-for-you, code-for-sam, code-for-jo`. Deploy.
6. **Settings**, **Trigger Events** (older dashboards: **Triggers**), **Cron Triggers**, **Add**. Expression `* * * * *` (every minute).
7. Open the Worker address (`https://coverwatch.<you>.workers.dev`) in a browser. It should say "Cover Watch alerts is running."
8. On the phone, in Cover Watch: **...** menu, **Settings**, **Lock-screen alerts**. Enter the address and the access code, tap **Turn on**, allow notifications, then **Send a lock-screen test**.

## Limits on the free plan

Workers Free allows 10 ms of CPU per run, 50 outside requests per run, and 1,000 KV writes per day. The Worker only writes when something changed, only asks ESPN for the days your open bets are on, and takes turns between the big college scoreboards.

## Adding or removing people

- **Add:** edit the `TOKEN` secret (**Settings**, **Variables and Secrets**), add a new code after a comma, and deploy. Send the person the Worker address and their code. They install the app, open **Settings**, **Lock-screen alerts**, enter both and tap **Turn on**.
- **Remove:** delete that person's code from `TOKEN` and deploy. Their alerts stop within a minute and the helper refuses them. Anyone with no phone signed up for 30 days is tidied away automatically.
- **Everyone shares the free-plan limits** (the 1,000 KV writes per day, the 10 ms of CPU per run). It suits a handful of people. If the Cloudflare logs show "Exceeded CPU", the $5 a month Workers plan fixes it.
- Anyone who knows a valid code can use the helper, so share codes only with people you trust.
- Apps set up before the shared version have no ID. They make one by themselves the next time they open and sign up again. Re-paste the new `worker.js` once in step 2 above to upgrade the helper.
