import React from 'react';
import Button from '@mui/material/Button';
import Dropdown from './Dropdown';
import OffscreenNav from './OffscreenNav';

const App = () => {
  const options = ['Option 1', 'Option 2', 'Option 3'];

  return (
    <div>
      <OffscreenNav />
      <h1>Hello, World! from React</h1>
      <Dropdown options={options} />
      <Button variant="contained">Hello world</Button>
    </div>
  );
};

export default App;