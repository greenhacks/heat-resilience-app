function ClickCounter(props) {
  const [currentCount, setCurrentCount] = React.useState(props.initialCount);
  return (
    <div>
      <div>{currentCount}</div>
      {/* <button type="button" onClick={() => setCurrentCount(currentCount + 1)}>
        Click me to increase the count
      </button> */}
      <ClickComponent buttonClick={() => setCurrentCount(currentCount + 1)} />
    </div>
  );
}

function ClickComponent({buttonClick}) {
  return (
      <button type="button" onClick={buttonClick}>
        Click me to increase the count
      </button>
  );
}
// //useEffect - React hook (React 2 lecture notes)
// useEffect(() => {
//   // GET request using fetch inside useEffect React hook
//   fetch('alerts.json')
//       .then(response => response.json())
//       .then(data => setTotalReactPackages(data.total));

// // empty dependency array means this effect will only run once (like componentDidMount in classes)
// }, []);

ReactDOM.render(<ClickCounter />, document.querySelector('#root'));