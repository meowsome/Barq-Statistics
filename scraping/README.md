# Barq Statistics

How to set-up scraping
1. Make an account on Barq
2. Use a packet sniffer to determine what your Barq API Key is
3. Make .env file with the following: `barq_authorization=YOUR_API_KEY`
4. Set your profile to various locations and record the data that is sent with the POST request
5. Edit [locations.json](scraping/locations.json) with your locations that you recorded
6. Set up database by running [create_db.sql](scraping/create_db.sql)
6. Run [scrape.py](scraping/scrape.py)

---

### Fun Fact:
The Barq Terms states that you should not scrape in a way that negatively impacts site performance. This project has various delays implemented while the scraping is happening, and does not scrape fast enough to impact site performance.