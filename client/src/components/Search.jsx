import SearchIcon from "../assets/search_icon.png";
import { useState } from "react";

export default function Search({fetchSummaries}) {

  const baseUrl =  "http://127.0.0.1:5000";

  const wikiAPI =
    "https://en.wikipedia.org/w/api.php?action=opensearch&search=REPLACEME&limit=20&namespace=0&format=json&origin=*";

  const [results, setResults] = useState([]);
  const resultElements = results.map((result) => {
    return (
      <span className="search_result">
        <p onClick={() => fetchSummaries(result.link)}>{result.title}</p>
      </span>
    );
  });

  function searchWikis(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const newSearch = formData.get("wiki_search");
    const searchResults = [];

    const url = wikiAPI.replace("REPLACEME", newSearch);

    fetch(url)
      .then((res) => res.json())
      .then(function (data) {
        for (let i = 0; i < data[1].length; i++) {
          searchResults.push({ title: data[1][i], link: data[3][i] });
        }
        setResults(searchResults);
      });

    event.currentTarget.reset();
  }

  return (
    <div className="search">
      <form className="search_bar" onSubmit={searchWikis} method="post">
        <input
          type="text"
          placeholder="e.g. Marvel Cinematic Universe"
          name="wiki_search"
        ></input>
        <button>
          <img src={SearchIcon}></img>
        </button>
      </form>
      {resultElements}
    </div>
  );
}
