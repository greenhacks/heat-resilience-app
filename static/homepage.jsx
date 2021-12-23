//attempting React - using React 1 demo code

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
  
  ReactDOM.render(<ClickCounter initialCount={10} />, document.querySelector('#root'));
  