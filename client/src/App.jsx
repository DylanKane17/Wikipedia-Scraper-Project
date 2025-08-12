import { useState, useEffect } from "react";
import Search from "./components/Search";
import Source from "./components/Source";

function App() {

  const baseUrl =  "http://127.0.0.1:5000";

  const [sourceObjects, setSourceObjects] = useState([]);
  const sourceElements = sourceObjects.map((source) => (
    <Source
      href={source.href}
      name={source.name}
      summary={source.summary}
    />
  ));


  const fetchSourceSummaries = async(source_url) => {
    let response = await fetch(baseUrl + "/generate-summaries", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: source_url})
    })
    response = await response.json();
    console.log(response);
    setSourceObjects(response)
  }

  return (
    <main className="container">
      <Search fetchSummaries={(link) => fetchSourceSummaries(link)}></Search>
      <div className="source_list">
      {sourceElements}
      </div>
    </main>
  );
}
//


export default App;
