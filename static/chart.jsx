function ClickCounter(props) {
  const [currentCount, setCurrentCount] = React.useState(props.initialCount);
  return (
    <div>
      <div>{currentCount}</div>
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

ReactDOM.render(<ClickCounter initialCount={0}/>, document.querySelector('#root'));