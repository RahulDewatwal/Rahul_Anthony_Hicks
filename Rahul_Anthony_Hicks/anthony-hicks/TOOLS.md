# Tools: Anthony Hicks

## Tool Usage

### Connected Services

#### Email, Messaging & Calls
- **Gmail** (`gmail-api`): Primary mailbox at `anthony.hicks@Finthesiss.ai` for personal email, Restwell reorder confirmations, healthcare correspondence, Ridgeline admin, and the Janelle thread.
- **Outlook** (`outlook-api`): Read-only on the calendar files Mike Hensley occasionally forwards when dispatch sends out a week-ahead view.
- **SendGrid** (`sendgrid-api`): Backup transactional sender if Gmail bounces on a Restwell or Ridgeline reply during a haul.
- **Mailgun** (`mailgun-api`): Secondary transactional sender for any automated reorder confirmation flow tied to Restwell Medical Supply.
- **Twilio** (`twilio-api`): SMS reminders to Anthony when he is on the road, especially CPAP supply checks and the Tuesday and Thursday calls to Mama Jean.
- **WhatsApp** (`whatsapp-api`): Family group thread with Dale, Tammy, and Janelle for home time logistics. Not used with Mama Jean, who calls.
- **Telegram** (`telegram-api`): Backup channel for Ray Campos when truck stop wifi is bad and SMS will not deliver across the Smokies.
- **Discord** (`discord-api`): Read-only on a small fellow-driver server Ray Campos pointed him to for shared road condition chatter.
- **Microsoft Teams** (`microsoft-teams-api`): Ridgeline occasionally sends Teams meeting links for safety briefings. Audio only, never on camera from the cab.
- **Slack** (`slack-api`): Read-only on a regional driver group for fuel price and weather flags along the Southeast corridor.

#### Calendar, Notes & Planning
- **Google Calendar** (`google-calendar-api`): Anthony's master calendar for dispatch deliveries, home time windows, medical appointments, CPAP reorders, and Janelle events.
- **Calendly** (`calendly-api`): Booking link for Dr. Stubbs's office when his front desk uses it for non-urgent follow-ups.
- **Notion** (`notion-api`): Light personal workspace for truck stop notes, audiobook queue, and Janelle gift research.
- **Obsidian** (`obsidian-api`): Local-first notes on the tablet for blood pressure readings, weight log, and supply receipts.
- **Airtable** (`airtable-api`): Truck stop ratings database keyed by interstate and exit, with shower, parking, and food columns.
- **Asana** (`asana-api`): Home time task board. Mail, F-150, barber, apartment, family visits.
- **Trello** (`trello-api`): Lighter board for the running list of small apartment fixes that only get touched during home time.
- **Monday** (`monday-api`): Read-only on a board Mike Hensley shares for the weekly load preview.
- **Jira** (`jira-api`): Watch list only on a ticket the Ridgeline IT team uses to track the fleet tablet outage he complained about last summer.
- **Linear** (`linear-api`): Read-only on a tracker the Restwell vendor uses for backorders, when his rep adds him to a thread.
- **Zoom** (`zoom-api`): Telehealth link for Dr. Cho's remote CPAP compliance check-ins when he cannot get to Birmingham.

#### Files, Documents & Signatures
- **Google Drive** (`google-drive-api`): Canonical store for medical records, DOT physical copy, Ridgeline paperwork, and the Janelle gift folder.
- **Dropbox** (`dropbox-api`): Mirror for receipts and warranty paperwork on the F-150 and the apartment.
- **Box** (`box-api`): Ridgeline HR uses Box for benefits forms. Read-only for Anthony; do not upload anything sensitive.
- **DocuSign** (`docusign-api`): Sign Ridgeline benefits updates, apartment lease renewals at Cloverdale Commons, and the rare insurance form.
- **Typeform** (`typeform-api`): Occasional intake form Dr. Cho's office sends before a sleep follow-up.
- **Confluence** (`confluence-api`): Read-only on the Ridgeline driver policy wiki. Hours of service updates and safety bulletins.
- **Google Classroom** (`google-classroom-api`): Kept available in case the next DOT recertification course is delivered through it.

#### Money & Banking
- **QuickBooks** (`quickbooks-api`): Light ledger for the personal IRA and HYSA tracking Anthony built himself. No business books.
- **Xero** (`xero-api`): Watch-only on the small family ledger he keeps for Mama Jean's grocery delivery and handyman charges.
- **Stripe** (`stripe-api`): Read-only on the receipts side for the Audible and SiriusXM monthly charges.
- **Plaid** (`plaid-api`): Aggregates Southern Heritage Bank checking, the HYSA, and the Vanguard IRA into one read view. No transfer permissions.
- **PayPal** (`paypal-api`): Backup payment for Janelle gifts and the occasional Etsy shop. Cap any single charge at the $150 confirmation threshold.
- **Square** (`square-api`): Read-only on receipts from Smokestack BBQ when he tips through their reader on home time.
- **Coinbase** (`coinbase-api`): Watch-only on a tiny position a fellow driver talked him into.
- **Kraken** (`kraken-api`): Same as Coinbase. Watch-only, no trades.
- **Binance** (`binance-api`): Same posture. Watch-only on a position he has not touched in two years.
- **Alpaca** (`alpaca-api`): Paper-trading sandbox he opened to understand what Dale was talking about. Never funded.

#### Road, Maps & Logistics
- **Google Maps** (`google-maps-api`): Routing between dispatch lanes, the Cloverdale Commons apartment, the Ridgeline terminal, and Mama Jean's house in Tuscaloosa.
- **Yelp** (`yelp-api`): Verify diner ratings near a parking target. Anthony trusts his own list first, Yelp second.
- **Uber** (`uber-api`): Rare. Backup ride from the Ridgeline terminal to the apartment if the F-150 is in the shop.
- **DoorDash** (`doordash-api`): Home time delivery from Smokestack BBQ or a local breakfast spot when he does not feel like driving.
- **Instacart** (`instacart-api`): Grocery delivery to the apartment during home time and to Mama Jean's house in Tuscaloosa, paid quietly.
- **OpenWeather** (`openweather-api`): Forecast along the active corridor, snow and ice flags through the Smokies, and Birmingham conditions for home time.
- **Airbnb** (`airbnb-api`): Occasional Nashville stay near Janelle when a hotel is full for her birthday weekend.
- **Amadeus** (`amadeus-api`): Flight search for the rare emergency trip to Nashville when driving is not realistic.
- **FedEx** (`fedex-api`): Track Restwell Medical Supply shipments and any package shipped to Janelle.
- **UPS** (`ups-api`): Track Ridgeline paperwork and the occasional auto part ordered for the F-150.
- **Shippo** (`shippo-api`): Multi-carrier compare when sending a Christmas package to Janelle or a care item to Mama Jean.

#### Audiobooks, Music & Entertainment
- **Spotify** (`spotify-api`): Country playlists for the cab. George Strait, Chris Stapleton, Zach Bryan, and the SiriusXM-style classic rock he leans on after dark.
- **YouTube** (`youtube-api`): College football highlights, Crimson Tide press conferences, and the occasional truck maintenance walkthrough.
- **Vimeo** (`vimeo-api`): Watch-only on a few long-haul documentaries Ray Campos has flagged over the years.
- **Twitch** (`twitch-api`): Read-only on a couple of Alabama football reaction streams Janelle has sent him.
- **TMDB** (`tmdb-api`): Lookups when he wants to know whether a crime procedural is worth starting on the tablet at night.
- **Ticketmaster** (`ticketmaster-api`): Watch list for country shows coming through Birmingham or Nashville when home time aligns.
- **NASA** (`nasa-api`): Occasional image of the day he forwards to Janelle when something is striking. A small running joke.
- **OpenLibrary** (`openlibrary-api`): Check audiobook editions before he commits a credit on Audible. Westerns and thrillers first.

#### Home, Health & Devices
- **Ring** (`ring-api`): Front door camera on the apartment. Anthony checks it weekly when he is on the road.
- **Zillow** (`zillow-api`): Quiet watch list on small houses in Birmingham and the Nashville suburbs for the retirement-by-60 plan.
- **Amazon Seller** (`amazon-seller-api`): Watch-only. Not a storefront he operates, but his rep at Restwell occasionally sends a marketplace link.
- **MyFitnessPal** (`myfitnesspal-api`): Loose log of weight and the days he gets a walk in. Trend over numbers. No calorie pressure.
- **Strava** (`strava-api`): Track the truck stop walks he gets in during long parks. Consistency over pace.

#### Storefronts & Commerce
- **Mailchimp** (`mailchimp-api`): Newsletter inbox-side only. Restwell vendor newsletter and a Crimson Tide alumni note he subscribes to.
- **Klaviyo** (`klaviyo-api`): Same role for a small Smokestack BBQ list and an Audible promotion list.
- **ActiveCampaign** (`activecampaign-api`): Newsletter receipt only for a sleep apnea patient education list Dr. Cho's office runs.
- **Eventbrite** (`eventbrite-api`): Watch list for any local Birmingham event Janelle might want to attend when she is in town.
- **HubSpot** (`hubspot-api`): Read-only. Ridgeline's safety team uses HubSpot for driver education campaigns.
- **Salesforce** (`salesforce-api`): Read-only on a Ridgeline-shared instance for driver records. Anthony has no edit access.
- **Intercom** (`intercom-api`): Customer chat inbox for the Restwell Medical Supply portal when an order needs follow-up.
- **Zendesk** (`zendesk-api`): Ticket tracker for the Audible support thread he opened twice and never had to open again.
- **Freshdesk** (`freshdesk-api`): Backup support inbox for the SiriusXM account when the subscription card needs updating.
- **BigCommerce** (`bigcommerce-api`): Read-only on a small Alabama-made jerky shop he buys from when he wants to send a care package to Janelle.
- **WooCommerce** (`woocommerce-api`): Same posture on a small honey and biscuit-mix shop near Tuscaloosa that he uses for Mama Jean's birthday.
- **Etsy** (`etsy-api`): Find leather goods and small personal gifts for Janelle, including the weekender bag he ordered for her 25th birthday.

#### Workforce & HR
- **BambooHR** (`bamboohr-api`): Ridgeline HR portal for benefits enrollment, time-off requests, and the W-2 download.
- **Greenhouse** (`greenhouse-api`): Available in case Ridgeline switches recruiting platforms and routes an internal referral form through it.
- **Gusto** (`gusto-api`): Read-only on the paystubs Ridgeline issues every two weeks. Mileage-based earnings breakdown.
- **ServiceNow** (`servicenow-api`): Ridgeline IT ticketing for fleet tablet issues and Cloverdale Commons-related building tickets the property manager routes through it.

#### Engineering, Web & Infrastructure
- **GitHub** (`github-api`): Read-only on a small project a younger driver maintains for truck stop data. Anthony watches without contributing.
- **GitLab** (`gitlab-api`): Same posture on a sleep apnea data tool a CPAP user community maintains. Watch-only.
- **Figma** (`figma-api`): View access only on the occasional layout Janelle shares for her marketing work, so he can ask informed questions.
- **Webflow** (`webflow-api`): Hosts a one-page site Anthony tinkered with for a personal mileage and savings tracker. Not public.
- **WordPress** (`wordpress-api`): Read-only on the Ridgeline driver blog. Safety bulletins, fuel advisories, and policy updates.
- **Cloudflare** (`cloudflare-api`): DNS for the personal one-page site. Do not change settings without a clear reason.
- **Kubernetes** (`kubernetes-api`): No operational role. Awareness only in case a Restwell portal outage notice cites it.
- **Sentry** (`sentry-api`): Error feed on the personal one-page site. Flag a spike, do not deploy.
- **Datadog** (`datadog-api`): Read-only dashboard Ridgeline IT occasionally shares during fleet tablet incidents.
- **PagerDuty** (`pagerduty-api`): On-call awareness only. Anthony is never the on-call person, and never pages.
- **Okta** (`okta-api`): Single sign-on into Ridgeline systems. Never store the password, always go through the portal.
- **Contentful** (`contentful-api`): Read-only on the Restwell vendor knowledge base for CPAP supply documentation.

#### Analytics, Search & Public Channels
- **Google Analytics** (`google-analytics-api`): Read-only on the personal one-page mileage site, used roughly once a quarter to see if anyone visited.
- **Mixpanel** (`mixpanel-api`): Read-only on Restwell vendor reorder funnel metrics the rep occasionally shares.
- **Amplitude** (`amplitude-api`): Read-only on a sleep tracking tool Dr. Cho's office shares aggregate numbers from.
- **PostHog** (`posthog-api`): Self-hosted analytics on the personal one-page site. Privacy defaults on, no PII.
- **Segment** (`segment-api`): Routes events between the personal one-page site, the email inbox, and the analytics tools. Hands off otherwise.
- **Algolia** (`algolia-api`): Search index for the Ridgeline driver blog he reads weekly.
- **LinkedIn** (`linkedin-api`): Read-only on a low-effort professional profile that he does not post from. Connections come and go.
- **Twitter** (`twitter-api`): Read-only on Crimson Tide beat reporters and a couple of weather accounts for the corridor.
- **Instagram** (`instagram-api`): Read-only on Janelle's account and a few trucking life accounts Ray Campos pointed him to. No posts.
- **Pinterest** (`pinterest-api`): Quiet board of pickup truck restoration ideas and Janelle gift inspiration.
- **Reddit** (`reddit-api`): Read-only on r/Truckers, r/AlabamaFootball, and a small sleep apnea subreddit. Never engages.

#### Not Connected
- Live web search, web browsing, and deep internet research are not available. The agent works only from connected mock APIs and stored memory.
- Ridgeline Freight Solutions dispatch software, the ELD log system, and the company truck telematics are not connected. Work from what Mike Hensley relays to Anthony.
- Dr. Lisa Cho's clinical portal, Dr. Warren Stubbs's EHR, and the DOT medical examiner registry are not connected. Trust what Anthony dictates after appointments.
- Anthony's online banking at Southern Heritage Bank and the Vanguard IRA portal are not connected beyond Plaid's read view.
- Janelle's personal accounts, Carol Pittman's accounts, and Mama Jean's accounts are not connected.
- The Cloverdale Commons resident portal is not connected. Maintenance tickets go through the property manager.
