async function getPUUID(gameName, tagLine, region) {
  const url = "https://us-central1-lolstudy.cloudfunctions.net/get_puuid";

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        game_name: gameName,
        tag_line: tagLine,
        region: region,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Error fetching PUUID:", errorText);
      alert("Error fetching PUUID: " + errorText);
      return null;
    }

    const data = await response.json();
    return data.puuid;
  } catch (err) {
    console.error("Fetch error:", err);
    alert("Fetch error: " + err.message);
    return null;
  }
}

document.getElementById("fetchButton").addEventListener("click", async () => {
  const gameName = document.getElementById("summonerName").value.trim();
  const tagLine = document.getElementById("tagLine").value.trim();
  const region = document.getElementById("region").value;

  if (!gameName || !tagLine || !region) {
    alert("Please enter Summoner Name, Tag Line, and select Region.");
    return;
  }

  const puuid = await getPUUID(gameName, tagLine, region);
  if (puuid) {
    console.log("PUUID:", puuid);
    alert("PUUID retrieved! Check console for details.");
  }
});
