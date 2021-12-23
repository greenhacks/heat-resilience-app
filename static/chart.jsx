// import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
// const data = [{name: 'Page A', alert: 400}];

// // const renderLineChart = (
// //   <LineChart width={400} height={400} data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
// //     <Line type="monotone" dataKey="alert" stroke="#8884d8" />
// //     <XAxis dataKey="name" />
// //     <YAxis />
// //     <Tooltip />
// //   </LineChart>
// // );

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

function Hello() {
  return (
    <ul>
      <li>Hi World!</li>
    </ul>
  );
}



ReactDOM.render(<ClickCounter />, document.querySelector('#root'));