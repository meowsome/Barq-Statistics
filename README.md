# Barq Statistics

### How to set-up scraping
1. Make an account on Barq
2. Use a packet sniffer to determine what your Barq API Key is
3. Make .env file with the following: `barq_authorization=YOUR_API_KEY`
4. Set your profile to various locations and record the data that is sent with the POST request
5. Put `profile_overview` and `profile_detail` GraphQL requests as entries in [bodies.json](scraping/bodies.json)
6. Edit [locations.json](scraping/locations.json) with your locations that you recorded
7. Set up a Mongodb database
8. Run [scrape.py](scraping/scrape.py)


### How to Generate Static Site:
1. Ensure database is started
2. cd server/express
3. node index
4. cd ../barq-scraping-react-app
5. node scripts/cache-api.js
6. npm run build
7. npx serve out