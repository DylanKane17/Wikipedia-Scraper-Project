export default function Source(props) {
  return <div className="source_list">
    <div className="source_list_container">
    <a href={props.href}>{props.name}</a> 
    <p>{props.summary}</p>
  </div>
  </div>;
}
