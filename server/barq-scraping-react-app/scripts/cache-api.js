import fs from "node:fs/promises";

async function cache(endpoint) {
    const data = await fetch("http://localhost:8080/api/" + endpoint).then(r => r.json());

    await fs.writeFile(
        `data/${endpoint}.json`,
        JSON.stringify(data)
    );
}

await cache("coordinates");
await cache("sonas-per-country");
await cache("fursonas");
await cache("age");
await cache("hobbies");
await cache("count");
await cache("genders");
await cache("orientation");
await cache("relationship");